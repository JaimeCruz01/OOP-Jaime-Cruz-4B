"""Exportación de productos a CSV, TXT, JSON y PDF.

Las dependencias y toda la lógica de archivos están confinadas en este módulo.
"""
from abc import ABC, abstractmethod
from collections.abc import Mapping
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable
import csv
import json
from fpdf import FPDF

PRODUCT_FIELDS = ("id", "nombre", "precio", "cantidad", "descripcion")


def _value(record: Mapping, *names):
    for name in names:
        if name in record:
            return record[name]
    return ""


def _normalize_product(product: Any) -> dict:
    """Admite dict_row de psycopg y tuplas del Modelo."""
    if isinstance(product, Mapping):
        return {
            "id": _value(product, "id", "id_producto", "product_id"),
            "nombre": _value(product, "nombre", "name", "producto"),
            "precio": _value(product, "precio", "price"),
            "cantidad": _value(product, "cantidad", "stock", "quantity"),
            "descripcion": _value(product, "descripcion", "description"),
        }
    if isinstance(product, (tuple, list)):
        if len(product) < 4:
            raise ValueError("Cada producto debe incluir al menos ID, nombre, precio y cantidad.")
        # Orden del SELECT del Modelo: id, nombre, precio, cantidad, descripcion.
        return {
            "id": product[0],
            "nombre": product[1],
            "precio": product[2],
            "cantidad": product[3],
            "descripcion": product[4] if len(product) > 4 else "",
        }
    raise TypeError("Cada producto debe ser un diccionario o una tupla/lista.")


def _normalize_products(data: Iterable[Any]) -> list[dict]:
    if data is None:
        raise ValueError("No se recibieron datos para exportar.")
    return [_normalize_product(item) for item in data]


def _display(value):
    if value is None:
        return ""
    if isinstance(value, Decimal):
        return format(value, "f")
    return str(value)


def _json_default(value):
    if isinstance(value, Decimal):
        return str(value)  # conserva la precisión monetaria
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"No se puede convertir {type(value).__name__} a JSON.")


def _pdf_text(value):
    # Las fuentes base de FPDF 1.7.2 usan Latin-1.
    return _display(value).replace("\r", " ").replace("\n", " ").encode(
        "latin-1", errors="replace"
    ).decode("latin-1")


class Exporter(ABC):
    extension = ""

    @abstractmethod
    def export(self, data: Iterable[Any], file_path: str | Path) -> None:
        raise NotImplementedError("La subclase debe implementar export().")


class CSVExporter(Exporter):
    extension = ".csv"

    def export(self, data, file_path):
        products = _normalize_products(data)
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8-sig") as stream:
            writer = csv.DictWriter(stream, fieldnames=PRODUCT_FIELDS)
            writer.writeheader()
            for product in products:
                writer.writerow({key: _display(product[key]) for key in PRODUCT_FIELDS})


class TXTExporter(Exporter):
    extension = ".txt"

    def export(self, data, file_path):
        products = _normalize_products(data)
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as stream:
            stream.write("--- REPORTE DE PRODUCTOS ---\n")
            stream.write(f"Total de productos: {len(products)}\n\n")
            for p in products:
                stream.write(
                    f"ID: {_display(p['id'])} | Nombre: {_display(p['nombre'])} | "
                    f"Precio: ${_display(p['precio'])} | Cantidad: {_display(p['cantidad'])} | "
                    f"Descripción: {_display(p['descripcion'])}\n"
                )


class JSONExporter(Exporter):
    extension = ".json"

    def export(self, data, file_path):
        products = _normalize_products(data)
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as stream:
            json.dump(products, stream, ensure_ascii=False, indent=4, default=_json_default)
            stream.write("\n")


class PDFExporter(Exporter):
    extension = ".pdf"

    def export(self, data, file_path):
        products = _normalize_products(data)
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        pdf = FPDF(orientation="L", unit="mm", format="A4")
        pdf.set_auto_page_break(auto=True, margin=12)
        pdf.add_page()

        def headers():
            pdf.set_font("Arial", "B", 15)
            pdf.cell(270, 10, "Reporte de inventario de productos", ln=1, align="C")
            pdf.ln(4)
            pdf.set_font("Arial", "B", 9)
            widths = (15, 55, 30, 25, 145)
            for label, width in zip(("ID", "Nombre", "Precio", "Cantidad", "Descripción"), widths):
                pdf.cell(width, 9, label, border=1, align="C")
            pdf.ln()

        headers()
        pdf.set_font("Arial", size=8)
        if not products:
            pdf.cell(270, 9, "No hay productos registrados.", border=1, ln=1)
        for p in products:
            if pdf.get_y() > 180:
                pdf.add_page()
                headers()
                pdf.set_font("Arial", size=8)
            values = (
                _pdf_text(p["id"])[:10],
                _pdf_text(p["nombre"])[:30],
                "$" + _pdf_text(p["precio"])[:16],
                _pdf_text(p["cantidad"])[:12],
                _pdf_text(p["descripcion"])[:85],
            )
            for value, width in zip(values, (15, 55, 30, 25, 145)):
                pdf.cell(width, 8, value, border=1)
            pdf.ln()
        pdf.output(str(path))


_EXPORTERS = {
    "CSV": CSVExporter,
    "TXT": TXTExporter,
    "JSON": JSONExporter,
    "PDF": PDFExporter,
}


def create_exporter(format_name: str) -> Exporter:
    normalized = str(format_name or "").strip().upper()
    exporter = _EXPORTERS.get(normalized)
    if exporter is None:
        raise ValueError("Formato no válido. Selecciona CSV, TXT, JSON o PDF.")
    return exporter()

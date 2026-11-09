"""Pruebas del módulo de exportación; no requieren PostgreSQL ni Tkinter."""
import csv
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from exporters import Exporter, create_exporter


SAMPLE_PRODUCTS = [
    {
        "id": 1, "nombre": "Café de olla", "precio": Decimal("25.50"),
        "stock": 12, "descripcion": "Café tradicional",
    },
    {
        "id": 2, "nombre": "Piñata", "precio": Decimal("150.00"),
        "stock": 4, "descripcion": "Piñata de siete picos",
    },
]


class ExporterTests(unittest.TestCase):
    def test_base_exporter_is_abstract(self):
        with self.assertRaises(TypeError):
            Exporter()

    def test_all_formats_create_files_with_real_fields(self):
        extensions = {"CSV": ".csv", "TXT": ".txt", "JSON": ".json", "PDF": ".pdf"}
        with tempfile.TemporaryDirectory() as folder:
            for fmt, extension in extensions.items():
                with self.subTest(format=fmt):
                    path = Path(folder) / f"productos{extension}"
                    create_exporter(fmt).export(SAMPLE_PRODUCTS, path)
                    self.assertTrue(path.is_file())
                    self.assertGreater(path.stat().st_size, 0)
                    content = path.read_bytes()
                    if fmt == "PDF":
                        self.assertTrue(content.startswith(b"%PDF-"))
                    elif fmt == "JSON":
                        data = json.loads(content.decode("utf-8"))
                        self.assertEqual(data[0]["descripcion"], "Café tradicional")
                        self.assertEqual(data[0]["cantidad"], 12)
                    elif fmt == "CSV":
                        rows = list(csv.DictReader(content.decode("utf-8-sig").splitlines()))
                        self.assertEqual(rows[0]["descripcion"], "Café tradicional")
                        self.assertEqual(rows[0]["cantidad"], "12")
                    else:
                        text = content.decode("utf-8")
                        self.assertIn("Café tradicional", text)
                        self.assertIn("Cantidad: 12", text)

    def test_database_column_names_are_supported(self):
        product = {
            "id_producto": 8, "nombre": "Monitor", "precio": Decimal("2999.00"),
            "cantidad": Decimal("7"), "descripcion": "Monitor 24 pulgadas",
        }
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "productos.json"
            create_exporter("JSON").export([product], path)
            exported = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(exported[0]["id"], 8)
            self.assertEqual(exported[0]["cantidad"], "7")
            self.assertEqual(exported[0]["descripcion"], "Monitor 24 pulgadas")

    def test_tuple_rows_are_supported(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "productos.txt"
            create_exporter("TXT").export(
                [(3, "Producto de prueba", Decimal("9.90"), 5, "Descripción")], path
            )
            content = path.read_text(encoding="utf-8")
            self.assertIn("ID: 3", content)
            self.assertIn("Descripción: Descripción", content)

    def test_factory_rejects_unknown_format(self):
        with self.assertRaises(ValueError):
            create_exporter("XML")

    def test_factory_is_case_insensitive(self):
        self.assertEqual(create_exporter("pdf").extension, ".pdf")


if __name__ == "__main__":
    unittest.main()

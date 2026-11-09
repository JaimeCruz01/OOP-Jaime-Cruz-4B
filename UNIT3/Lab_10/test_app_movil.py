"""Pruebas automatizadas de la práctica Lab 10 con pytest."""

import pytest

from app_movil import (
    PerfilMovil,
    PerfilPro,
    PuntosInsuficientesError,
    SuscripcionExpiradaError,
)


@pytest.fixture
def perfil():
    """Proporciona un perfil base nuevo e independiente para cada prueba."""
    return PerfilMovil("usuario_prueba")


def test_atributos_iniciales(perfil):
    assert perfil.username == "usuario_prueba"
    assert perfil.gemas == 50
    assert perfil.racha_dias == 1
    assert perfil.notificaciones_activas is True


def test_no_permite_gemas_iniciales_negativas():
    with pytest.raises(ValueError):
        PerfilMovil("usuario", gemas=-1)


@pytest.mark.parametrize("cantidad", [1, 5, 25, 100])
def test_ganar_gemas_incrementa_balance(perfil, cantidad):
    resultado = perfil.ganar_gemas(cantidad)
    assert resultado == 50 + cantidad
    assert perfil.gemas == 50 + cantidad


@pytest.mark.parametrize("cantidad", [0, -1, -20])
def test_ganar_gemas_rechaza_cantidades_no_positivas(perfil, cantidad):
    with pytest.raises(ValueError):
        perfil.ganar_gemas(cantidad)
    assert perfil.gemas == 50


@pytest.mark.parametrize("cantidad", [1.5, "10", True])
def test_ganar_gemas_rechaza_tipos_invalidos(perfil, cantidad):
    with pytest.raises(ValueError):
        perfil.ganar_gemas(cantidad)
    assert perfil.gemas == 50


def test_gastar_gemas_resta_balance(perfil):
    resultado = perfil.gastar_gemas(20)
    assert resultado == 30
    assert perfil.gemas == 30


def test_gastar_todas_las_gemas(perfil):
    assert perfil.gastar_gemas(50) == 0


@pytest.mark.parametrize("cantidad", [0, -1])
def test_gastar_gemas_rechaza_cantidades_no_positivas(perfil, cantidad):
    with pytest.raises(ValueError):
        perfil.gastar_gemas(cantidad)
    assert perfil.gemas == 50


def test_gastar_gemas_rechaza_saldo_insuficiente(perfil):
    with pytest.raises(PuntosInsuficientesError):
        perfil.gastar_gemas(51)
    assert perfil.gemas == 50


def test_gemas_no_pueden_asignarse_con_valor_negativo(perfil):
    with pytest.raises(ValueError):
        perfil.gemas = -10
    assert perfil.gemas == 50


def test_perfil_pro_hereda_de_perfil_movil():
    perfil_pro = PerfilPro("usuario_pro", meses_suscripcion=3)
    assert isinstance(perfil_pro, PerfilMovil)
    assert isinstance(perfil_pro, PerfilPro)
    assert perfil_pro.gemas == 50
    assert perfil_pro.meses_suscripcion == 3
    assert perfil_pro.es_pro is True


@pytest.mark.parametrize("meses", [0, -1, -12])
def test_perfil_pro_rechaza_suscripcion_inicial_no_positiva(meses):
    with pytest.raises(ValueError):
        PerfilPro("usuario_pro", meses_suscripcion=meses)


def test_descarga_offline_con_suscripcion_vigente():
    perfil_pro = PerfilPro("usuario_pro", meses_suscripcion=2)
    mensaje = perfil_pro.descargar_contenido_offline()
    assert isinstance(mensaje, str)
    assert "autorizada" in mensaje
    assert perfil_pro.es_pro is True


def test_suscripcion_expirada_desactiva_estado_pro_y_lanza_excepcion():
    perfil_pro = PerfilPro("usuario_pro", meses_suscripcion=1)
    perfil_pro.meses_suscripcion = 0

    with pytest.raises(SuscripcionExpiradaError):
        perfil_pro.descargar_contenido_offline()

    assert perfil_pro.es_pro is False
    assert perfil_pro.meses_suscripcion == 0


def test_perfil_pro_no_puede_descargar_despues_de_expirar():
    perfil_pro = PerfilPro("usuario_pro", meses_suscripcion=1)
    perfil_pro.meses_suscripcion = 0

    with pytest.raises(SuscripcionExpiradaError):
        perfil_pro.descargar_contenido_offline()

    with pytest.raises(SuscripcionExpiradaError):
        perfil_pro.descargar_contenido_offline()


def test_perfil_pro_conserva_funciones_de_gemas():
    perfil_pro = PerfilPro("usuario_pro", meses_suscripcion=4)
    assert perfil_pro.ganar_gemas(10) == 60
    assert perfil_pro.gastar_gemas(15) == 45

# Lab 10. Automated Testing with pytest

Práctica de Programación Orientada a Objetos: perfiles móviles, herencia,
encapsulación, excepciones personalizadas y pruebas automatizadas.

## Contenido

- `app_movil.py`: excepciones `SuscripcionExpiradaError` y
  `PuntosInsuficientesError`, clase base `PerfilMovil` y subclase `PerfilPro`.
- `test_app_movil.py`: pruebas con fixture, `pytest.raises`,
  `pytest.mark.parametrize` y `isinstance`.
- `requirements.txt`: dependencia de pytest.
- `pytest.ini`: configuración de descubrimiento de pruebas.

## Requisitos

Python 3.8 o superior.

## Instalación en Windows PowerShell

Desde la carpeta `Lab_10`, ejecuta:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell bloquea la activación del entorno virtual, puedes instalar y
lanzar pytest con el intérprete global o ejecutar los comandos usando
`.venv\Scripts\python.exe`.

## Ejecutar la suite solicitada

```powershell
python -m pytest -v
```

El resultado esperado es que todas las pruebas aparezcan como `PASSED`.

## Reglas implementadas

- `PerfilMovil` inicia con 50 gemas, racha de 1 día y notificaciones activas.
- El saldo de gemas no admite valores negativos.
- `ganar_gemas` y `gastar_gemas` requieren cantidades enteras estrictamente
  positivas.
- `gastar_gemas` lanza `PuntosInsuficientesError` cuando el saldo no alcanza.
- `PerfilPro` hereda de `PerfilMovil` y requiere una suscripción inicial mayor
  que cero meses.
- `descargar_contenido_offline` autoriza la operación si la suscripción está
  vigente. Al llegar `meses_suscripcion` a cero, desactiva `es_pro` y lanza
  `SuscripcionExpiradaError`.

Nota: una descarga no consume meses. El método valida el estado de la
suscripción; el componente que controle el paso del tiempo debe actualizar
`meses_suscripcion` cuando corresponda. Esto evita tratar cada descarga como
si transcurriera un mes, comportamiento que no especifica la guía.

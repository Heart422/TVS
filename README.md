# Administrador de Videos TVS

Aplicación simple para administrar y reproducir videos organizados por procesos desde una carpeta compartida en red.

## Archivos incluidos

- `app.py` – servidor Python/Flask
- `index.html` – frontend de la aplicación
- `processes.json` – nombres de procesos configurables
- `requirements.txt` – dependencias de Python

## Requisitos

- Python 3.11+ instalado
- Flask instalado (`pip install -r requirements.txt`)
- Acceso a la carpeta compartida de red donde se guardan los videos

## Cómo correr la aplicación

1. Abre PowerShell en la carpeta del proyecto.
2. Instala dependencias:

```powershell
python -m pip install -r requirements.txt
```

3. Ejecuta el servidor:

```powershell
python app.py
```

4. Abre tu navegador en:

```text
http://127.0.0.1:5000
```

> Si quieres acceder desde otra PC en la misma red, usa la IP del host en vez de `127.0.0.1`.

## Configuración de la carpeta de videos

Por defecto `app.py` está configurado para usar la carpeta de red:

```python
\\cofs04\Gindustrial\Industrial\TV´S Lean
```

Puedes cambiarla con la variable de entorno `VIDEO_SHARE_PATH` si prefieres otra ruta:

```powershell
$env:VIDEO_SHARE_PATH='\\SERVIDOR\Compartido\Videos'
python app.py
```

## Procesos configurados

Los procesos están definidos en `processes.json`:

- `Emulsiones`
- `Hidroalcoholes`
- `Maquillajes`
- `Otros`

Cada proceso corresponde a una carpeta dentro de la ruta de red.

## Notas para GitHub

- No incluyas archivos de video en el repositorio.
- No incluyas carpetas generadas como `__pycache__`.
- Este repositorio es solo el código y la configuración.

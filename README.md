# Project 1

Web Programming with Python and JavaScript

## Instalacion entorno virtual
- Crea la carpeta :
py -3 -m venv .venv
- activa el entorno virtual:
 .venv\Scripts\activate
- Instala los requerimientos:
pip install -r .\requirements.txt 
- variable de entorno:
set FLASK_APP=application.py
$env:FLASK_APP = "application.py"
set DATABASE_URL="enlace"
$env:DATABASE_URL = ""

database url from postgres:// to postgresql:// solved the problem.

flask run
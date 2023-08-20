# Project 1: Books
 Web Programming with Python and JavaScript

## Instalación entorno virtual
### Crea la carpeta : 
>`py -3 -m venv .venv`   
### Activa el entorno virtual:
> `.venv\Scripts\activate`
### Instala los requerimientos: 
> `pip install -r .\requirements.txt`
## Variables de entorno:
### Asigna el valor a la variable de entorno FLASK_APP 
>`$env:FLASK_APP = "application.py"`
### Asigna el valor a la variable de entorno DATABASE_URL
>`$env:DATABASE_URL = "URL"` 

&nbsp;&nbsp;&nbsp; URL es el enlace a tu base de datos en la nube.

&nbsp;&nbsp;&nbsp; si usas una base de datos postgres en render edita en enlace que render te brinda de la siguiente manera:

>`database url from postgres:// to postgresql://`

## Corre la aplicación web
>`flask run`
# Project 1: Books
 Web Programming with Python and JavaScript
## Información del proyecto
- Titulo:  `Books`
- Autor:  `Jerry Ronaldo Espino Inestroza`
- Descripción: Proyecto 1 de programación web. Se basa en un sitio web que nos muestras libros y sus reseñas, haciendo uso de la API de Goolge. En este sitio los usuarios son capaces de registrarse, loggearse, buscar libros y ver reseñas de otros usuarios.
<!--- Video: [video]()-->

## 🛠 Skills
- HTML
- CSS
- Flask
- Postgresql
- Bootstrap

## Detalles del proyecto
### Requerimientos solicitados
- [x] Registro: Los usuarios deberían ser capaces de registrarse en tu sitio web, proveyendo (como mínimo) un nombre de usuario y una contraseña.
- [x] Inicio de Sesión: Los usuarios, una vez registrados, deberían ser capaces de iniciar sesión en tu sitio web con su nombre de usuario y contraseña.
- [x] Cierre de sesión: Los usuarios conectados deberían ser capaces de cerrar sesión.


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


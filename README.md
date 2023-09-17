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
- [x] En un archivo Python llamado import.py separado de tu aplicación web, escriba un programa que tome los libros y los importe a su base de datos PostgreSQL
- [x] Búsqueda: Una vez que el usuario ha iniciado sesión, deberían ser llevados a una página donde puedan buscar un libro.
- [x] Pagina de Libro Cuando los usuarios hagan click en un libro entre los resultados de la página de búsqueda, deberían ser llevados a una página de libro, con detalles sobre el libro: su título, autor, año de publicación, número ISBN, y cualquier reseña que los usuarios han dejado para ese libro en tu sitio web.
- [x] Envío de Reseña: En la página de libro, los usuarios deberían ser capaces de enviar una reseña: consistiendo en un puntaje en una escala del 1 al 5, al igual que un componente de texto para la reseña donde el usuario pueda escribir su opinión sobre un libro. Los usuarios no deberían ser capaces de enviar múltiples reseñas para el mismo libro.
    
    Para lograr quu un usuario no pueda hacer mas de una reseña en un libro agregamos una restricción en la tabla ratigns al crearla. El restricción especifica es: `unique(user_id, libro_id)`. Esto es una restricción que asegura que la combinación de los valores en las columnas user_id y libro_id sea única en toda la tabla. Es decir, no puedes tener dos filas en la tabla que tengan el mismo user_id y libro_id. Cada par user_id, libro_id debe ser único, esto nos ayuda a evitar duplicados. Esto se encuentra en el archivo **crearTablas.py**
- [x] Información de Reseña de Goodreads (Google Books API): En la página de libro, también deberías mostrar (si está disponible) el puntaje promedio y cantidad de puntuaciones que el libro ha recibido de Goodreads.
- [x] Acceso a API: Si los usuarios hacen una solicitud GET a la ruta /api/ de tu sitio web, donde es un número ISBN, tu sitio web debería retornar una respuesta JSON conteniendo el título del libro, autor, fecha de publicación, número ISBN, conteo de reseñas, y puntaje promedio. El JSON resultante debería seguir el siguiente formato:
>
    {
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
    }

- [x] Deberías estar usando comandos SQL puros (a través del método execute de SQLAlchemy) para hacer consultas a la base de datos. No deberías usar el ORM de SQLAlchemy (si te es familiar) para este proyecto.
- [x] En README.md , incluye una breve descripción de tu proyecto, qué contiene cada archivo, y (opcionalmente) cualquier otra información adicional que el staff deba saber acerca de tu proyecto.
- [x] Si has añadido algún paquete Python que necesite ser instalado para poder ejecutar tu aplicación web, ¡asegúrate de añadirlo a requirements.txt!
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

### Importa los libros del csv a la base de datos
>`python import.py`

### Crea las tablas necesarias para el funcionamiento de la web
>`python crearTablas.py`

## Corre la aplicación web
>`flask run`


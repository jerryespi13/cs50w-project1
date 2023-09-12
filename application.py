import os
# para hacer peticiones a una URL
import requests
# Flask
from flask import Flask, session, render_template, request, flash, redirect, jsonify, abort
# para el manejo de las sesiones
from flask_session import Session
# para el manejo de la base de datos
from sqlalchemy import create_engine, text, bindparam, String, Integer
from sqlalchemy.orm import scoped_session, sessionmaker
# para contraseñas hasheadas
from werkzeug.security import check_password_hash, generate_password_hash
# archivo propio
from helpers import *

# para variables de entornos
from dotenv import load_dotenv
# Cargamos nuestras variables de entorno
load_dotenv()

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Define el número máximo de intentos que se hará una consulta a la DB
max_attempts = 5

@app.route("/")
def index():
    return redirect("/login")

@app.route("/register", methods=["GET","POST"])
def register():
    """Ruta para registrar un usuario"""
    if request.method == "GET":
        # si el usuario ya inicio sesion no puede ir a la ruta register
        if "user_id" in session:
            flash("Cierra sesión primeramente")
            return redirect('/search')
        return render_template("register.html")
    
    else:
        # obtenemos los datos del formulario
        nombre = request.form.get("name")
        usuario = request.form.get("username")
        contraseña = request.form.get("password")
        confirmacion_contraseña = request.form.get("confirmation")

        # nos aseguramos que todos los datos se hayan ingresedo
        # en los campos del formulario
        if not nombre:
            flash("Introducir campo nombre")
            return render_template("register.html")
        elif not usuario:
            flash("Ingrese campo usuario")
            return render_template("register.html")
        elif not contraseña:
            flash("Ingrese campo contraseña")
            return render_template("register.html")
        elif not confirmacion_contraseña:
            flash("Ingrese campo confirmacion contraseña")
            return render_template("register.html")
        elif contraseña != confirmacion_contraseña:
            flash("Contraseñas deben de ser iguales")
            return render_template("register.html")

        # confirmamos que el usuario no exista
        # hacemos la consulta SQL
        """
            Aqui uso un bucle for por que en momentos render no responde a la consulta, entonces lo intento
            unas cuantas veces mas hasta max_attempts veces
        """
        for _ in range(max_attempts):
            try:
                query = text(
                                """
                                    SELECT * FROM usuarios WHERE usuario = :usuario
                                """
                            )
                # pasamos los parametros
                query = query.bindparams(bindparam("usuario", type_=String()))
                # ejecutamos la consulta
                resultado = db.execute(query, {"usuario":usuario}).fetchall()
                # Si la consulta se ejecuta correctamente se confirma la transacion y salimos del bloque for
                db.commit()
                break
            except Exception as e:
                # si ocurre una excepcion, revierte la transaccion y se intenta de nuevo gracias al for
                print("Ocurrió un error por parte de render, pero lo sulucionamos")
                db.rollback()
        # cerramos la conexion
        db.close()
        
        # comparamos el resultado de la columna usuario en la db 
        # devuelto por la consulta con el usuario ingresado por el usuario
        
        if len(resultado) != 0:
            # si el usuario existe lo notificamos para que elija otro nombre de usuario
            if resultado[0].usuario == usuario:
                flash('Usuario ya existe')
                return render_template("register.html")
        
        # si el usuario no existe guardamos los datos en la DB
        # generando un hash para la contraseña ingresada
        contraseña_segura = generate_password_hash(contraseña)

        # creamos nuestra query
        """
            Aqui uso un bucle for por que en momentos render no responde a la consulta, entonces lo intento
            unas cuantas veces mas hasta max_attempts veces
        """
        for _ in range(max_attempts):
            try:
                query = text(
                                """
                                    INSERT INTO usuarios (nombre, usuario, contraseña)
                                    VALUES (:nombre, :usuario, :contraseña);
                                """
                            )
                # vinculamos variables
                query.bindparams(
                                    bindparam("nombre", type_=String()),
                                    bindparam("usuario", type_=String()),
                                    bindparam("contraseña", type_=String())
                                )
                # asignamos variables y ejecutamos nuestra query
                db.execute(query,{"nombre":nombre, "usuario":usuario, "contraseña":contraseña_segura})
                # si la consulta se ejecuta correctamente confirmamos la transacion y salimos del bloque for
                resultado = db.commit()
                break
            except Exception as e:
                # si ocurre una excepcion, revierte la transaccion y se intenta de nuevo gracias al for
                print("Ocurrió un error por parte de render pero lo sulucionamos")
                db.rollback()
        # cerramos la conecion
        db.close()

        # despues que el usario se registre lo redireccionamos al login
        return redirect("/login")

@app.route("/login", methods=["GET","POST"])
def login():
    """Ruta para iniciar session"""
    if request.method == "GET":
        # si el usuario ya inicio sesion no puede ir a la ruta login
        if "user_id" in session:
            flash("Si quieres iniciar sesión con otra cuenta, cierra esta sesión primeramente")
            return redirect('/search')
        return render_template("login.html")
    
    else:
        usuario = request.form.get("username")
        contraseña = request.form.get("password")
        if not usuario:
            flash("Introducir campo usuario")
            return render_template("login.html")
        elif not contraseña:
            flash("Introducir campo contraseña")
            return render_template("login.html")
        
        """
            Aqui uso un bucle for por que en momentos render no responde a la consulta, entonces lo intento
            unas cuantas veces mas hasta max_attempts veces
        """
        for _ in range(max_attempts):
            try:
                query = text(
                            """
                                SELECT * FROM usuarios WHERE usuario = :usuario 
                            """
                            )
                query.bindparams(bindparam("usuario", type_=String()))
                resultado = db.execute(query, {"usuario":usuario}).fetchone()
                # si la consulta se ejecuta correctamente confirmamos la transaccion y salimos del bloque for
                db.commit()
                break
            except Exception as e:
                # si ocurre una excepcion, revierte la transaccion y se intenta de nuevo gracias al for
                print("Ocurrió un error por parte de render pero lo solucionamos")
                db.rollback()
        db.close()
        if resultado == None or not check_password_hash(resultado.contraseña, contraseña):
            flash("Usuario o Contraseña incorrecto")
            return redirect("/login")

        # creamos la session del usuario
        session["user_id"] = resultado.id
        session["user_name"] = resultado.usuario
        session["name"] = resultado.nombre
        return redirect("/search")
    
# ruta para cerrar session
@app.route("/logout")
def logout():
    """Ruta para cerrar session"""
    # Borramos todas las variables de session
    session.clear()
    # Redirigimos a la pagina de inicio
    return redirect("/")

@app.route("/search", methods=["GET","POST"])
@login_required
def search():
    # pintamos la pagina de busqueda
    if request.method == "GET":
        return render_template("search.html")
    
    # recibimos la busqueda a realizar
    else:
        # obtenemos el parametro a buscar
        parametro = request.form.get("search").lower()
        # si no ingresaron nada lo hacemos saber
        if not parametro:
            flash("No ingresó ningún término de búsqueda")
            return render_template("search.html")
        
        # buscamos que exista en nuestra DB
        """
            Aqui uso un bucle for por que en momentos render no responde a la consulta, entonces lo intento
            unas cuantas veces mas hasta max_attempts veces
        """
        for _ in range(max_attempts):
            try:
                query_libros = text (
                                        """
                                            SELECT * FROM libros WHERE LOWER(title) LIKE :parametro OR isbn LIKE :parametro OR LOWER(author) LIKE :parametro
                                        """
                                    )
                query_libros.bindparams(bindparam("parametro", type_=String()))
                libro = db.execute(query_libros, {"parametro": '%{}%'.format(parametro)}).fetchall()
                # Si la consulta se ejecuta correctamente confirma la transacion
                db.commit()
                break
            except Exception as e:
                # si ocurre una excepcion, revierte la transaccion
                print("Ocurrió un error por parte de render pero lo sulucionamos")
                db.rollback()
        # cerramos la conexion
        db.close()

            
        # si la consulta al DB no devuelve nada, el libro no existe en nuestra DB
        if len(libro) == 0:
            flash("Libro no encontrado")
            return render_template("search.html")
        return render_template("search.html", libros=libro)

# para autocompletado
@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    """
    funcion que sirve para el autocompletado de busqueda
    """
    # obtenemos lo que el usuario a digitado en la barra de busqueda
    q = request.args.get("q")
    try:
        # buscamos los libros que tengan la coincidencia con lo que el usuario esta digitando
        query_obtener_libros = text("SELECT DISTINCT title FROM libros WHERE lower(title) LIKE :title LIMIT 5")
        query_obtener_libros.bindparams(bindparam("title", type_=String()))
        datos = db.execute(query_obtener_libros,{"title": '%{}%'.format(q)}).fetchall()
        db.commit()
        db.close()
    except Exception as e:
        error = "server closed the connection unexpectedly [Culpa a render]"
        return render_template("error.html", error=error , mensaje=e)
    # tranformamos a una lista la respuesta de la bd
    libros = []
    for dato in datos:
        libros.append(dato.title) 
    # respondemos con ese resultado
    return libros

@app.route("/verlibro", methods=["GET","POST"])
@login_required
def verlibro():
    isbn = request.args.get("isbn")
    if request.method == "GET":
        # verificamos que el libro en la DB
        """
        Aqui uso un bucle for por que en momentos render no responde a la consulta, entonces lo intento
        unas cuantas veces mas hasta max_attempts veces
        """
        for _ in range(max_attempts):
            try:
                query_libro = text("SELECT id, isbn FROM libros WHERE isbn = :isbn")
                query_libro.bindparams(bindparam("isbn", type_=String()))
                libro = db.execute(query_libro,{"isbn":isbn}).fetchone()
                # si la consulta se ejecuta correctamente se confirma la transaccion y salimos del bloque for
                db.commit()
                break
            except Exception as e:
                # si ocurre una excepcion, revierte la transaccion
                print("Ocurrió un error por parte de render pero lo sulucionamos")
                db.rollback()
        # cerramos la conexion
        db.close()
        if libro:
            response = []
            
            # pedimos los datos del libro a la API de Google books
            datos = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:"+libro.isbn)

            # si la respuesta es un codigo 429, error: 429 To many requests
            if datos.status_code == 429:
                abort(datos.status_code)
            
            # si la respuesta es un codigo 200 quiere decir que la peticion fue respondida correctamente
            if datos.status_code == 200:
                datos = datos.json()
                if "items" in datos:
                    response.append(datos['items'][0]['volumeInfo'])

            # datos de reseñas
            libro_id = int(libro.id)
            """
            Aqui uso un bucle for por que en momentos render no responde a la consulta, entonces lo intento
            unas cuantas veces mas hasta max_attempts veces
            """
            for _ in range(max_attempts):
                try:
                    query_reseñas = text(
                                            """
                                                SELECT ratings.comentario, ratings.puntuacion, to_char(ratings.created_at, 'DD/MM/YY') AS fecha, usuarios.nombre, usuarios.usuario
                                                FROM ratings
                                                INNER JOIN usuarios ON ratings.user_id = usuarios.id
                                                WHERE ratings.libro_id = :libro_id
                                                ORDER BY fecha DESC
                                            """
                                        )
                    query_reseñas.bindparams(bindparam("libro_id", type_=Integer()))
                    reseñas = db.execute(query_reseñas, {"libro_id":libro_id}).fetchall()
                    # si la consulta se ejecuta correctamente se confirma la transaccion y salimos del bloque for
                    db.commit()
                    break
                except Exception as e:
                    # si ocurre una excepcion, revierte la transaccion
                    print("Ocurrió un error por parte de render pero lo sulucionamos")
                    db.rollback()
                # cerramos la conexion
                db.close()

            # verificamos si el usuario ya hizo una reseña en el libro
            review = False
            for reseña in reseñas:
                # si ya la hizo mandamos TRUE en la variable reseña, si no mandamos False
                if session['user_name'] in reseña:
                    review = True
            return render_template("verLibro.html", response=response, reseñas=reseñas, libro_id=libro_id, review=review)   

        # si por get meten un isbn que no existe retornamos un error
        else:
            return render_template("error.html", error="Libro no existe"), 404
    # metodo POST [Por aqui ingresamos la reseñas]
    else:
        # capturamos datos
        puntuacion = int(request.form.get("start"))
        mensaje = request.form.get("mensaje")
        libro_id = int(request.form.get("libro_id"))

        # Query para insertar reseña
        """
        Aqui uso un bucle for por que en momentos render no responde a la consulta, entonces lo intento
        unas cuantas veces mas hasta max_attempts veces
        """
        for _ in range(max_attempts):
            try:
                query_insertar_reseña = text(
                                            """
                                                INSERT INTO ratings(user_id, libro_id, comentario, puntuacion)
                                                VALUES(:user_id, :libro_id, :mensaje, :puntuacion)
                                            """
                                            )
                query_insertar_reseña.bindparams(
                                                    bindparam("user_id", type_=Integer()),
                                                    bindparam("libro_id", type_=Integer()),
                                                    bindparam("mensaje", type_=String()),
                                                    bindparam("puntuacion", type_=Integer())
                                                )

                db.execute(query_insertar_reseña,{"user_id":session['user_id'], "libro_id":libro_id, "mensaje":mensaje, "puntuacion":puntuacion})
                # si la consulta se ejecuta correctamenteo confirmamos la transaccion y salimos del bucle for
                db.commit()
                break
            except Exception as e:
                # si ocurre una excepcion, revierte la transaccion y se vuele a interntar gracias al for
                print(e)
                db.rollback()

        # Retornamos a la pagina del mismo libro
        url = "/verlibro?isbn=" + isbn
        return redirect(url)

@app.route("/api/<isbn>")
def api(isbn):
    try:
        for _ in range(max_attempts):
            query_api = text(
                            """
                                SELECT libros.isbn, libros.title, libros.author, libros.year,
                                COALESCE(to_char(AVG(ratings.puntuacion),'9.99'), '0') AS average_score,
                                COUNT(ratings.puntuacion) AS review_count
                                FROM libros
                                LEFT OUTER JOIN ratings ON libros.id = ratings.libro_id
                                WHERE libros.isbn = :isbn
                                GROUP BY libros.id
                            """
                            )
            query_api.bindparams(bindparam("isbn", type_=String()))
            datos_libro = db.execute(query_api, {"isbn":isbn}).fetchone()
            # si la consulta se ejecuta correctamenteo confirmamos la transaccion y salimos del bucle for
            db.commit()
            break
    except Exception as e:
        # si ocurre una excepcion, revierte la transaccion y se vuele a interntar gracias al for
        print("Ocurrió un error por parte de render pero lo sulucionamos")
        db.rollback()

    if datos_libro is None:
        return render_template("error.html", error="Libro no existe"), 404
    libro_JSON = {}
    for dato in datos_libro._fields:
        libro_JSON[dato] = datos_libro._get_by_key_impl_mapping(dato)
    return jsonify(libro_JSON)

# Error 404 Página no encontrada
@app.errorhandler(404)
def page_not_found(error):
    mensaje = "Por favor verifica que tu direccion URL sea la correcta"
    return render_template("error.html", error="Página no encontrada...", mensaje = mensaje), 404

# Error 429 To many requeste
@app.errorhandler(429)
def to_many_requests(error):
    mensaje="""
                Quota exceeded for quota metric 'Queries' and limit 'Queries per day' of service 'books.googleapis.com'
                for consumer. "reason": "rateLimitExceeded"
            """
    return render_template("error.html", error="books.googleapis error: 429", mensaje=mensaje), 429
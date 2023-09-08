import os
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

import werkzeug

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
        query = text(
                        """
                            SELECT * FROM usuarios WHERE usuario = :usuario
                        """
                    )
        # pasamos los parametros
        query = query.bindparams(
                                    bindparam("usuario", type_=String())
                                )
        # ejecutamos la consulta
        resultado = db.execute(query, {"usuario":usuario}).fetchall()
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
        
        resultado = db.commit()
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
        query = text(
                    """
                        SELECT * FROM usuarios WHERE usuario = :usuario 
                    """
                    )
        query.bindparams(
            bindparam("usuario", type_=String())
        )
        resultado = db.execute(query, {"usuario":usuario}).fetchone()
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
        query_libros = text (
                                """
                                    SELECT * FROM libros WHERE LOWER(title) LIKE :parametro OR isbn LIKE :parametro OR LOWER(author) LIKE :parametro
                                """
                            )
        query_libros.bindparams(bindparam("parametro", type_=String()))
        libro = db.execute(query_libros, {"parametro": '%{}%'.format(parametro)}).fetchall()
        db.close()
        # si la consulta al DB no devuelve nada, el libro no existe en nuestra DB
        if len(libro) == 0:
            flash("Libro no encontrado")
            return render_template("search.html")
        return render_template("search.html", libros=libro)

@app.route("/listalibros", methods=["GET"])
def listalibros():
    """
    devuelve en JSON un listado de los libros para hacer uso de autocomplete
    """
    query_obtener_libros = text("SELECT title FROM libros")
    datos = db.execute(query_obtener_libros).fetchall()
    db.close()
    libros = []
    for dato in datos:
        libros.append(dato.title)   
    return jsonify({"libros":libros})

@app.route("/verlibro", methods=["GET","POST"])
@login_required
def verlibro():
    isbn = request.args.get("isbn")
    if request.method == "GET":
        # verificamos que el libro en la DB
        query_libro = text("SELECT id, isbn FROM libros WHERE isbn = :isbn")
        query_libro.bindparams(bindparam("isbn", type_=String()))
        libro = db.execute(query_libro,{"isbn":isbn}).fetchone()
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
        db.commit()

        # Retornamos a la pagina del mismo libro
        url = "/verlibro?isbn=" + isbn
        return redirect(url)


@app.route("/api/<isbn>")
def api(isbn):
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
    db.close()
    if datos_libro is None:
        return render_template("error.html", error="Libro no existe"), 404
    libro_JSON = {}
    for dato in datos_libro._fields:
        libro_JSON[dato] = datos_libro._get_by_key_impl_mapping(dato)
    return jsonify(libro_JSON)

# Error 404 Página no encontrada
@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404

# Error 429 Página no encontrada
@app.errorhandler(429)
def to_many_requests(error):
    return render_template("error.html", error="books.googleapis error: 429"), 429
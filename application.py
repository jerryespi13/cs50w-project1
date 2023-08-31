import os
# Flask
from flask import Flask, session, render_template, request, flash, redirect, jsonify
# para el manejo de las sesiones
from flask_session import Session
# para el manejo de la base de datos
from sqlalchemy import create_engine, text, bindparam, String
from sqlalchemy.orm import scoped_session, sessionmaker
# para contraseñas hasheadas
from werkzeug.security import check_password_hash, generate_password_hash
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
    if request.method == "GET":
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
        # despues que el usario se registre lo redireccionamos al login
        return redirect("/login")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
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
        
        print(resultado)
        # creamos la session del usuario
        session["user_id"] = resultado.id
        session["name"] = resultado.nombre
        return redirect("/search")
    
# ruta para cerrar session
@app.route("/logout")
def logout():
    """Log user out"""
    # Borramos todas las variables de session
    session.clear()
    # Redirigimos a la pagina de inicio
    return redirect("/")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/listalibros", methods=["GET"])
def listalibros():
    """
    devuelve en JSON un listado de los libros para hacer uso de autocomplete
    """
    query_obtener_libros = text("SELECT title FROM libros")
    datos = db.execute(query_obtener_libros).fetchall()
    libros = []
    for dato in datos:
        libros.append(dato.title)   
    return jsonify({"libros":libros})
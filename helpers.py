from functools import wraps
from flask import redirect, session, flash
import os

# para el manejo de la base de datos
from sqlalchemy import create_engine, text, bindparam, String, Integer
from sqlalchemy.orm import scoped_session, sessionmaker

# Define el número máximo de intentos que se hará una consulta a la DB
max_attempts = 5

# extensiones permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# para variables de entornos
from dotenv import load_dotenv
# Cargamos nuestras variables de entorno
load_dotenv()

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash('Inicia Sessión')
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    """
    funcion que verifica si la extension del archivo a subir esta permitida
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def actualizarVariablesSession():
    for _ in range(max_attempts):
            try:
                query = text("SELECT * FROM usuarios WHERE id = :id ")
                query.bindparams(bindparam("id", type_=String()))
                resultado = db.execute(query, {"id":session['user_id']}).fetchone()
                # si la consulta se ejecuta correctamente confirmamos la transaccion y salimos del bloque for
                db.commit()
                break
            except Exception as e:
                # si ocurre una excepcion, revierte la transaccion y se intenta de nuevo gracias al for
                print("Ocurrió un error por parte de render pero lo solucionamos")
                db.rollback()
    # creamos la session del usuario
    session["user_id"] = resultado.id
    session["user_name"] = resultado.usuario
    session["name"] = resultado.nombre
    session["img"] = resultado.img
import os

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

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
    return render_template("layout.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    else:
        # TO DO
        #query = text("SELECT * FROM usuarios")
        #datos = db.execute(query).fetchall()
        #print(datos)
        nombre = request.form.get("name")
        usuario = request.form.get("username")
        contraseña = request.form.get("password")
        confirmacion_contraseña = request.form.get("confirmation")
        print(nombre + " " + usuario + " " + contraseña + " "+ confirmacion_contraseña)
        return "Hacer Metodo POST"

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    else:
        #TO DO
        return "Hacer Metodo POST"
    
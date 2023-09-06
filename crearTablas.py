import os
# para el manejo de la base de datos
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

# para variables de entornos
from dotenv import load_dotenv
# Cargamos nuestras variables de entorno
load_dotenv()

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# creamos la tabla usaurio si no existe
query_crear_tabla_usuarios = text(
                                    """
                                        CREATE TABLE IF NOT EXISTS "usuarios" (
                                                                                "id" serial primary key,
                                                                                "nombre" varchar(255) not null,
                                                                                "usuario" varchar(255) not null,
                                                                                "contraseña" varchar(255) not null,
                                                                                "img" varchar(255) not null default '/static/images/avatar.png',
                                                                                "created_at" timestamp not null default NOW()
                                                                                )
                                    """
                                 )
db.execute(query_crear_tabla_usuarios)
db.commit()

# creamos la tabla usaurio si no existe
query_crear_tabla_ratings = text(
                                   """
                                          CREATE TABLE IF NOT EXISTS "ratings"(
                                                                                    "id" serial primary key,
                                                                                    "user_id" int,
                                                                                    "libro_id" int,
                                                                                    "comentario" varchar(255) not null,
                                                                                    "puntuacion" int not null,
                                                                                    "created_at" timestamp not null default NOW(),
                                                                                    constraint usuarios
                                                                                    foreign key(user_id) references usuarios(id),
                                                                                    constraint libros
                                                                                    foreign key(libro_id) references libros(id),
                                                                                    unique(user_id, libro_id)
                                                                             )
                                   """
                            )
db.execute(query_crear_tabla_ratings)
db.commit()
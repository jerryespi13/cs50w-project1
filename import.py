import os
# Para el manejo de archivos csv
import csv
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

# abrimos el archivo
with open("books.csv") as file:
    columnas = '"id" serial primary key, '
    field_names =""
    columnas_tabla =""
    # obtenemos algunos datos necesarios para la creacion de la tabla
    reader = csv.DictReader(file)
    for i in range(1, (len(reader.fieldnames) + 1)):
        columnas += '"' + reader.fieldnames[i - 1] + '" '  + "varchar(255) not null, "
        field_names += ":"+ reader.fieldnames[i - 1] + ', '
        columnas_tabla += reader.fieldnames[i - 1] + ', '
    # Creamos la tabla
    query_crear_tabla_libros = text(
                f"""
                CREATE TABLE IF NOT EXISTS "libros" ({columnas.removesuffix(', ')})
                """
            )
    db.execute(query_crear_tabla_libros)
    db.commit()

    # insertamos los datos del csv a la DB
    a = 1
    for datos in reader:
        query_insertar_datos_tabla_libros = text(
                                                f"""
                                                INSERT INTO libros ({columnas_tabla.removesuffix(", ")})
                                                VALUES ({field_names.removesuffix(", ")});
                                                """
                                            )
        # dos astericos (**) operador de desempaquetado
        db.execute(query_insertar_datos_tabla_libros,{**datos})
        print(f" Insertado: ({a}) {datos}")
        a +=1
    db.commit()
    print("Datos insertados correctamente")
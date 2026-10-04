from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
import os
import psycopg

app = FastAPI()


class Editorial(BaseModel):
    nombre: str
    pais: str


class Libro(BaseModel):
    titulo: str
    paginas: int = Field(gt=0)
    editorial: Editorial
    disponible: bool = True


class Autor(BaseModel):
    nombre: str


autores = [
    {"nombre": "George Orwell"},
    {"nombre": "Antoine de Saint-Exupéry"},
    {"nombre": "Jorge Luis Borges"}
]


def obtener_conexion():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        dbname=os.environ["DB_NAME"]
    )


@app.get("/")
def inicio():
    return {"mensaje": "hola"}


@app.get("/salud")
def salud():
    try:
        conexion = obtener_conexion()
        conexion.close()

        return {
            "estado": "ok",
            "base_de_datos": "conectada"
        }

    except Exception as error:
        return {
            "estado": "error",
            "detalle": str(error)
        }


@app.get("/libros", response_model=list[Libro])
def listar_libros():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT titulo, paginas, editorial_nombre,
               editorial_pais, disponible
        FROM libros
        """
    )

    filas = cursor.fetchall()

    cursor.close()
    conexion.close()

    libros = []

    for fila in filas:
        libros.append(
            {
                "titulo": fila[0],
                "paginas": fila[1],
                "editorial": {
                    "nombre": fila[2],
                    "pais": fila[3]
                },
                "disponible": fila[4]
            }
        )

    return libros


@app.post("/libros", status_code=201, response_model=Libro)
def crear_libro(libro: Libro):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO libros
            (titulo, paginas, editorial_nombre, editorial_pais, disponible)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                libro.titulo,
                libro.paginas,
                libro.editorial.nombre,
                libro.editorial.pais,
                libro.disponible
            )
        )

        conexion.commit()

    except Exception as error:
        conexion.rollback()
        cursor.close()
        conexion.close()

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    cursor.close()
    conexion.close()

    return libro


@app.get("/libros/{titulo}", response_model=Libro)
def buscar_libro(titulo: str):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        SELECT titulo, paginas, editorial_nombre,
               editorial_pais, disponible
        FROM libros
        WHERE titulo = %s
        """,
        (titulo,)
    )

    fila = cursor.fetchone()

    cursor.close()
    conexion.close()

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )

    return {
        "titulo": fila[0],
        "paginas": fila[1],
        "editorial": {
            "nombre": fila[2],
            "pais": fila[3]
        },
        "disponible": fila[4]
    }


@app.delete("/libros/{titulo}", status_code=204)
def borrar_libro(titulo: str):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM libros WHERE titulo = %s",
        (titulo,)
    )

    if cursor.rowcount == 0:
        cursor.close()
        conexion.close()

        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )

    conexion.commit()
    cursor.close()
    conexion.close()

    return Response(status_code=204)


@app.get("/autores")
def listar_autores():
    return autores


@app.post("/autores", status_code=201)
def crear_autor(autor: Autor):
    autores.append(autor.model_dump())
    return autor
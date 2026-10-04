from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

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


libros = [
    {
        "titulo": "1984",
        "paginas": 328,
        "editorial": {
            "nombre": "Debolsillo",
            "pais": "España"
        },
        "disponible": True
    },
    {
        "titulo": "El principito",
        "paginas": 96,
        "editorial": {
            "nombre": "Salamandra",
            "pais": "España"
        },
        "disponible": True
    },
    {
        "titulo": "Ficciones",
        "paginas": 224,
        "editorial": {
            "nombre": "Emecé",
            "pais": "Argentina"
        },
        "disponible": True
    }
]


autores = [
    {"nombre": "George Orwell"},
    {"nombre": "Antoine de Saint-Exupéry"},
    {"nombre": "Jorge Luis Borges"}
]


@app.get("/")
def inicio():
    return {"mensaje": "hola"}


@app.get("/libros", response_model=list[Libro])
def listar_libros(paginas_min: int | None = None):
    if paginas_min is None:
        return libros

    libros_filtrados = []

    for libro in libros:
        if libro["paginas"] >= paginas_min:
            libros_filtrados.append(libro)

    return libros_filtrados


@app.post("/libros", status_code=201, response_model=Libro)
def crear_libro(libro: Libro):
    libros.append(libro.model_dump())
    return libro


@app.get("/libros/{titulo}", response_model=Libro)
def buscar_libro(titulo: str):
    for libro in libros:
        if libro["titulo"] == titulo:
            return libro

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


@app.put("/libros/{titulo}", response_model=Libro)
def actualizar_libro(titulo: str, libro_nuevo: Libro):
    for i in range(len(libros)):
        if libros[i]["titulo"] == titulo:
            libros[i] = libro_nuevo.model_dump()
            return libros[i]

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


@app.delete("/libros/{titulo}", status_code=204)
def borrar_libro(titulo: str):
    for i in range(len(libros)):
        if libros[i]["titulo"] == titulo:
            libros.pop(i)
            return Response(status_code=204)

    raise HTTPException(
        status_code=404,
        detail="Libro no encontrado"
    )


@app.get("/autores")
def listar_autores():
    return autores


@app.post("/autores", status_code=201)
def crear_autor(autor: Autor):
    autores.append(autor.model_dump())
    return autor
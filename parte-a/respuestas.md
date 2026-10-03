# Parte A — Imagen vs contenedor

## A1

Python del contenedor: 3.12.15  
Python de mi máquina: 3.14.3

El contenedor usa la versión de Python incluida en su imagen, independientemente de la instalada en la máquina.

## A2

Se levantaron dos contenedores (`python1` y `python2`) usando la misma imagen `python:3.12-slim`.

Esto demuestra que una sola imagen puede generar varios contenedores independientes.

## A3

`docker ps` muestra solo los contenedores en ejecución.

`docker ps -a` también muestra los contenedores que ya terminaron.

`docker logs` permite ver la salida de un contenedor aunque ya no esté corriendo.

## A4

Se creó un archivo dentro de un contenedor y luego se eliminó ese contenedor.

Al crear un nuevo contenedor desde la misma imagen, el archivo ya no existía.

Esto demuestra que los cambios realizados dentro de un contenedor no modifican la imagen y se pierden al eliminar ese contenedor.

## A5

Una imagen es una plantilla que contiene el programa y lo necesario para ejecutarlo, mientras que un contenedor es una instancia de esa imagen en ejecución.

Docker ayuda a evitar el problema de "en mi máquina anda y en la tuya no" porque ejecuta el programa dentro de un entorno definido y reproducible.

Un `venv` solo aísla las librerías de Python, mientras que Docker también permite definir la versión de Python, las dependencias, los archivos y el entorno necesario para ejecutar el programa.

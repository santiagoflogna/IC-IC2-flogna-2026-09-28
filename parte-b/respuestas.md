# Parte B — Dockerfile

## B2

No es necesario crear un `venv` dentro de la imagen porque el contenedor ya proporciona un entorno aislado para ejecutar la aplicación.

Las dependencias de Python se declaran en `requirements.txt` y se instalan dentro de la imagen mediante el `Dockerfile`.

## B3

Al eliminar la instalación de las dependencias, la imagen se construyó correctamente, pero el contenedor falló al ejecutarse con el siguiente error:

`ModuleNotFoundError: No module named 'requests'`

El error ocurre en runtime, porque durante el build el archivo `script.py` se copia pero no se ejecuta. El problema aparece cuando el contenedor inicia y Python intenta importar `requests`.

Se solucionó agregando nuevamente:

`RUN pip install --no-cache-dir -r requirements.txt`

## B4

La instrucción `RUN` se ejecuta durante la construcción de la imagen.

La instrucción `CMD` se ejecuta cada vez que se inicia un contenedor.

En este ejercicio, el `RUN` se ejecutó una vez durante el build y el `CMD` se ejecutó tres veces porque se realizaron tres `docker run`.

## B5

Cuando se construyó la imagen dos veces sin modificar archivos, Docker reutilizó las capas existentes mediante la caché.

Con el Dockerfile original:

`COPY . .`

`RUN pip install --no-cache-dir -r requirements.txt`

al modificar solamente `script.py`, Docker volvió a ejecutar la instalación de dependencias porque el cambio en `COPY . .` invalidó las capas siguientes.

Luego se reorganizó el Dockerfile de la siguiente manera:

`COPY requirements.txt .`

`RUN pip install --no-cache-dir -r requirements.txt`

`COPY script.py .`

De esta forma, si cambia solamente `script.py`, Docker puede reutilizar desde la caché la capa donde se instalaron las dependencias.

## B6

La imagen construida con `python:3.12` ocupó 1.62 GB, mientras que la construida con `python:3.12-slim` ocupó 206 MB.

La versión `slim` es más liviana porque contiene menos componentes del sistema. Conviene usarla cuando la aplicación no necesita herramientas adicionales, mientras que la imagen completa puede ser necesaria cuando el proyecto requiere más utilidades o dependencias del sistema.
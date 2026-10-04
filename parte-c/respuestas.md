# Parte C — Dockerizar una API

## C3

### C3-A

Se ejecutó el contenedor sin utilizar `-p`, aunque el Dockerfile tenía `EXPOSE 8000`.

Al intentar acceder desde la máquina con:

`curl.exe http://localhost:8000/docs`

se obtuvo el siguiente error:

`curl: (7) Failed to connect to localhost:8000 after 2234 ms: Could not connect to server`

La API estaba funcionando dentro del contenedor, pero el puerto no estaba publicado hacia la máquina. `EXPOSE` solamente documenta el puerto y no lo publica.

### C3-B

Se publicó el puerto con `-p 8000:8000`, pero Uvicorn se inició sin `--host 0.0.0.0`, por lo que escuchó en `127.0.0.1`.

Al intentar acceder desde la máquina se obtuvo:

`curl: (52) Empty reply from server`

`127.0.0.1` dentro del contenedor representa al propio contenedor. Para que la API pueda recibir conexiones provenientes desde afuera, Uvicorn debe escuchar en `0.0.0.0`.

## C4

Se agregó un archivo `.dockerignore` para evitar copiar archivos y carpetas innecesarias dentro de la imagen.

El archivo contiene:

`venv`  
`.venv`  
`.git`  
`__pycache__`  
`*.pyc`

Se verificó el contenido de la imagen y esas carpetas no fueron copiadas desde la máquina.

En este caso el tamaño de la imagen puede no cambiar de forma significativa porque esas carpetas no estaban presentes dentro del contexto de construcción.

Un `venv` creado en la máquina no es útil dentro del contenedor porque pertenece al entorno de la computadora local. Dentro de la imagen las dependencias se instalan nuevamente mediante `requirements.txt`.
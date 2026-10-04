# Parte D — Compose

## D1

Se creó un `compose.yaml` con dos servicios: la API y PostgreSQL.

La primera vez PostgreSQL se detuvo con el siguiente error:

`Database is uninitialized and superuser password is not specified.`

El problema era que la imagen de PostgreSQL necesitaba la variable `POSTGRES_PASSWORD` para poder inicializar la base.

Después de agregarla al `compose.yaml`, tanto la API como PostgreSQL quedaron en estado `Up`.

## D2

Se agregó un tercer servicio utilizando la imagen `eclipse-mosquitto:2`.

Los tres servicios pudieron levantarse juntos con:

`docker compose up -d`

De esta manera, Mosquitto no tuvo que instalarse en la computadora, sino que Docker descargó y ejecutó su imagen.

## D3

Se agregó el endpoint `GET /salud` para comprobar la conexión de la API con PostgreSQL mediante `psycopg`.

Los datos de conexión son leídos desde variables de entorno:

`DB_HOST`  
`DB_PORT`  
`DB_USER`  
`DB_PASSWORD`  
`DB_NAME`

La contraseña y los demás datos de conexión no están escritos directamente en el código Python.

La prueba de conexión devolvió:

`{"estado":"ok","base_de_datos":"conectada"}`

## D4

Se cambió temporalmente `DB_HOST` de `base` a `localhost`.

Al consultar `/salud`, se obtuvo un error de conexión a:

`127.0.0.1:5432`

Esto ocurre porque `localhost` dentro del contenedor de la API hace referencia al propio contenedor de la API y no al contenedor de PostgreSQL.

Se corrigió utilizando:

`DB_HOST: base`

`base` es el nombre del servicio de PostgreSQL dentro de la red creada por Docker Compose.

## D5

Primero se creó una tabla y una fila en PostgreSQL sin utilizar un volumen.

Después de ejecutar `docker compose down` y volver a levantar los servicios, la tabla ya no existía:

`ERROR: relation "prueba" does not exist`

Luego se agregó un volumen para PostgreSQL:

`postgres_data:/var/lib/postgresql/data`

Se creó nuevamente una tabla y una fila. Después de ejecutar `docker compose down` y volver a levantar los servicios, el dato continuó existiendo.

Esto demuestra que el volumen conserva los datos aunque el contenedor sea eliminado.

Finalmente, `docker compose down -v` eliminó también el volumen y los datos dejaron de existir.

## D6

Se modificaron `POST /libros` y `GET /libros` para utilizar PostgreSQL en lugar de una lista de Python.

Se cargó el libro:

`Docker para principiantes`

Luego se reinició solamente el contenedor de la API con:

`docker compose restart api`

Después del reinicio, `GET /libros` siguió devolviendo el libro.

Esto demuestra que los datos se encuentran almacenados en PostgreSQL y no dependen de la memoria del contenedor de la API.
# Parte E — Pub/Sub contra nuestro broker

## E1 — El broker que no contesta

Se probó la conexión al broker Mosquitto desde afuera de su contenedor.

Inicialmente, la versión utilizada ya permitía conexiones externas mediante su configuración, por lo que se modificó temporalmente `mosquitto.conf` para que escuchara solamente en localhost:

listener 1883 127.0.0.1
allow_anonymous true

Al intentar conectarse desde otro contenedor se obtuvo:

Error: Bad file descriptor

Esto ocurre porque `127.0.0.1` representa el localhost del propio contenedor del broker.

Después se corrigió la configuración:

listener 1883
allow_anonymous true

Con esta configuración, un cliente ejecutado desde otro contenedor pudo conectarse correctamente al broker.

El modo local es una medida de seguridad porque evita que otros equipos o contenedores puedan conectarse al broker hasta que se configure explícitamente un listener.

## E2 — La prueba que engaña

Se quitó temporalmente el montaje de `mosquitto.conf` y se realizaron las pruebas desde adentro del mismo contenedor del broker.

Suscriptor:

docker compose exec broker mosquitto_sub -h localhost -t biblio/prueba

Publicador:

docker compose exec broker mosquitto_pub -h localhost -t biblio/prueba -m "mensaje desde adentro"

El mensaje llegó correctamente.

Esto no demuestra que el broker acepte conexiones externas, porque tanto el publicador como el suscriptor están ejecutándose dentro del mismo contenedor del broker.

Para comprobar una conexión externa se debe utilizar otro contenedor, por ejemplo mediante `docker compose run`.

Finalmente se volvió a colocar el `mosquitto.conf`.

## E3 — Publicar y recibir

Se utilizaron dos terminales y dos contenedores externos al broker.

Suscriptor:

docker compose run --rm broker mosquitto_sub -h broker -t biblio/sala1/prestamo

Publicador:

docker compose run --rm broker mosquitto_pub -h broker -t biblio/sala1/prestamo -m "prestamo realizado"

El suscriptor recibió:

prestamo realizado

Esto demuestra que clientes externos al contenedor de Mosquitto pueden comunicarse con nuestro propio broker mediante la red de Docker Compose.

## E4 — El topic que no matchea

El suscriptor escuchó:

biblio/sala1/prestamo

Se probaron los siguientes topics:

biblio/Sala1/prestamo

No fue recibido porque MQTT distingue entre mayúsculas y minúsculas.

También se probó:

biblio/sala1/devolucion

Tampoco fue recibido porque el último nivel del topic es diferente.

Finalmente se publicó en:

biblio/sala1/prestamo

y el mensaje fue recibido correctamente.

Por lo tanto, sin utilizar wildcards, el topic debe coincidir exactamente carácter por carácter.

## E5 — Wildcards en acción

Primero se utilizó:

biblio/sala1/#

El wildcard `#` permite recibir todos los topics que comiencen con `biblio/sala1`, incluyendo los niveles que aparezcan después.

Por ejemplo, recibe:

biblio/sala1/prestamo
biblio/sala1/devolucion

pero no:

biblio/sala2/prestamo

Después se utilizó:

biblio/+/prestamo

El wildcard `+` reemplaza exactamente un nivel del topic.

Por lo tanto permite recibir:

biblio/sala1/prestamo
biblio/sala2/prestamo
biblio/sala3/prestamo

pero no recibe:

biblio/sala1/devolucion

La diferencia principal es:

# = uno o varios niveles desde ese punto.

+ = exactamente un nivel.
#!/bin/sh
# Este script es ejecutado por docker-compose antes de ejecutar el comando
# dentro de la instrucción command.
#
# Este script se encarga de correr las migraciones y la ubicación de
# los archivos son según donde se ejecute el archivo docker-compose.yml
#
# Ref: https://stackoverflow.com/a/41436850
#
# Autores: Fernando Pérez, Alejandra Cordero y Pablo Maldonado.
python ./banco-cliente/bancoCliente/manage.py makemigrations
python ./banco-cliente/bancoCliente/manage.py migrate
exec "$@"

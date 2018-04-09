# Dockerfile para el contenedor del banco del cliente.
#
# Este archivo contiene las directivas necesarias para crear una aplicación
# de Django que sirve de página web para el servidor.
#
# Autores: Fernando Pérez, Alejandra Cordero, Pablo Maldonado

# Obtener una imagen de python, específicamente con Python 3.6 instalado.
FROM python:3.6

# Hacer que la entrada y salida de Python no tenga buffer.
ENV PYTHONUNBUFFERED 1

# Crear la carpeta actual actual en el contenedor.
RUN mkdir /banco-cliente

# Setear la carpeta principal del contenedor.
WORKDIR /banco-cliente

# Añadir el archivo de requerimientos e instalarlos
COPY requirements.txt /banco-cliente/
RUN pip install -r requirements.txt

# Añadir el contenido de esta carpeta en el contenedor.
COPY . /banco-cliente/

# Copiar y cambiar los permisos el archivo que se encarga de las migraciones.
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Correr los comandos de migraciones
#RUN python3 /banco-cliente/bancoCliente/manage.py makemigrations
#RUN python3 /banco-cliente/bancoCliente/manage.py migrate

# CMD ["python3", "./banco-cliente/bancoCliente/manage.py runserver 0.0.0.0:8100"]

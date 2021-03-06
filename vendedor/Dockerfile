# Dockerfile para el contenedor del vendedor.
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
RUN mkdir /vendedor

# Setear la carpeta principal del contenedor. (hacer cd hasta acá.)
WORKDIR /vendedor

# Añadir el archivo de requerimientos e instalarlos
COPY requirements.txt /vendedor/
RUN pip install -r requirements.txt

# Añadir el contenido de esta carpeta en el contenedor.
COPY . /vendedor/

# Copiar y cambiar los permisos el archivo que se encarga de las migraciones.
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Movernos a la carpeta donde hacemos python manage.py
# WORKDIR /vendedor/ecommerce

# Correr los comandos de migraciones
# RUN python3 /vendedor/ecommerce/manage.py makemigrations
# RUN python3 /vendedor/ecommerce/manage.py migrate
EXPOSE 5090
# CMD ["gunicorn", "-b", "0.0.0.0:5090","ecommerce.wsgi:application"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:5090"]
CMD ["gunicorn", "-c", "config/gunicorn/conf.py", "--bind", ":5090", "--chdir", "ecommerce", "ecommerce.wsgi:application"]

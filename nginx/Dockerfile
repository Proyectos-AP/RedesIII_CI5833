# Dockerfile para el contenedor de NGINX.
#
# Este archivo contiene las directivas necesarias para configurar el servidor
# nginx junto con los certificados que debe servir.
#
# Autores: Fernando Pérez, Alejandra Cordero, Pablo Maldonado

# Obtener una imagen de python, específicamente con Python 3.6 instalado.
FROM nginx

# Pasar los proyectos de django 
RUN mkdir /nginx

# Crear la carpeta de los certificados
RUN mkdir /certificados

# Setear la carpeta principal del contenedor.
WORKDIR /nginx

# Borrar el sitio por defecto y añadir los sitios que nosotros especifiquemos.
RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/ /etc/nginx/sites-enabled

# Añadir el contenido de esta carpeta en el contenedor.
COPY . /vendedor/

# Copiar y cambiar los permisos el archivo que se encarga de las migraciones.
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Correr los comandos de migraciones
# RUN python3 /vendedor/ecommerce/manage.py makemigrations
# RUN python3 /vendedor/ecommerce/manage.py migrate

# CMD ["python3", "./vendedor/ecommerce/manage.py runserver 0.0.0.0:8000"]

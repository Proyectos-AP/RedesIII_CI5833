# Archivo de ayuda con Docker.

Referencias:
  - [Quickstart: Compose and Django](https://docs.docker.com/compose/django/)
  - [Dockerizing Django for Development](https://fernandofreitasalves.com/dockerizing-django-for-development/)
  - [Django development with Docker — A step by step guide](https://blog.devartis.com/django-development-with-docker-a-step-by-step-guide-525c0d08291)
  - [Deploying a full Django stack with Docker-Compose](https://www.capside.com/labs/deploying-full-django-stack-with-docker-compose/)
  - [Repo de Manuel Morejón](https://github.com/mmorejon/docker-django)

# Describir la app.
Crear un archivo `Dockerfile` que indique la imagen a utilizar y la configuración
que tendría esta imagen.

Abrir el archivo `Dockerfile` para visualizar cuál fue la solución.

# Composer
Se utiliza el comando `docker-compose` para hacer que la app corra como un servicio
y donde se tengan distintos servicios como por ejemplo, BD, NGINX, entre otros.

Para poder utilizar ese comando, debemos describir un archivo en `YAML` de configuración.
Éste se muestra en el archivo `docker-compose.yml`.

# Ejecución
Para ejecutar los contenedores junto con las aplicaciones deben ejecutarse
los dos siguientes comandos:
```bash
docker-compose build
docker-compose up
```

# Actualización.
Al estar trabajando con Django y Docker, todos los cambios a los que Django
les pueda aplicar un Hot Reload se verán automáticamente sin tener que volver a hacer Build.

Sin embargo, cambios que involucren tumbar el servidor de desarrollo, tendrán
que volverse a construir para que sean visibles (Ejecución). Un ejemplo de este tipo de cambios
es cuando se modifica el modelo de la BD.

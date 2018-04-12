# Aplicación web del vendedor

En este directorio se define la aplicación web correspondiente al sitio de comercio del vendedor.

## Docker
La aplicación está dentro de un contenedor de Docker y se ejecuta siguiendo
las instrucciones de `Dockerfile` y `docker-compose.yml`.

`Dockerfile` dice cuál es la imagen que se tomará, cuáles son las variables de
ambiente y los comandos necesarios para configurar la imagen.

`docker-compose.yml` expone la aplicación como un servicio, donde se configuran
las distintas aplicaciones, como NGINX, Bases de datos, Django y más.

## Instalación

### Instalación con *venv*
`venv` es un módulo de Python3.5+ que permite la creación de ambientes virtuales para Python y se convertirá en la manera estándar de crear ambientes.

1. Crear un ambiente virtual llamado `env`:
```bash
python3 -m venv env
```

2. Activar el ambiente virtual.
```bash
source env/bin/activate
```

3. Instalar los requerimientos.
```bash
  pip install --upgrade pip
  pip install -r requirements.txt
```

### Instalación con *virtualenv*

1. Crear un ambiente virtual con *virtualenv* en el directorio raíz del proyecto
``` bash
  virtualenv -p python3 env
```
2. Activar el ambiente virtual
``` bash
  source bin/env/activate
```
3. Instalar los requerimientos de la aplicación
``` bash
  pip install -r requirements.txt
```
4. Agrear el archivo de configuración llamado `config.json` dentro de `ecommerce/private/`. Éste se encuentra en la carpeta Drive del proyecto.

## Ejecución

1. Activar el ambiente virtual de *virtualenv*
``` bash
  source bin/env/activate
```
o

1. Activar el ambiente virtual de *venv*
``` bash
  source env/bin/activate
```

2. Ejecutar el servidor de *Django*
``` python
  python manage.py runserver
```

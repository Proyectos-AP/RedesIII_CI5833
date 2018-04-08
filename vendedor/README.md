# Aplicación web del vendedor

En este directorio se define la aplicación web correspondiente al sitio de comercio del vendedor.

## Docker
La aplicación está dentro de un contenedor de Docker y se ejecuta siguiendo
las instrucciones de `Dockerfile` y `docker-compose.yml`.

`Dockerfile` dice cuál es la imagen que se tomará, cuáles son las variables de
ambiente y los comandos necesarios para configurar la imagen.

`docker-compose.yml` expone la aplicación como un servicio, donde se configuran
las distintas aplicaciones, como NGINX, Bases de datos, Django y más.

### Instalación


# Instalación

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
4. Agregar como variable de ambiente el valor de la llave secreta para usar el captcha de Google. Para ello, abrir el archivo ~/.bashrc y agregar la siguiente línea
``` bash
  export CAPTCHA_SECRET_KEY=<clave_secreta>
```
  donde *clave_secreta* se encuentra en la carpeta Drive del proyecto.

5. Actualizar las variables de ambiente del sistema
``` bash
  source ~/.bashrc
```

# Ejecución

1. Activar el ambiente virtual
``` bash
  source bin/env/activate
```

2. Ejecutar el servidor de *Django*
``` python
  python manage.py runserver
```

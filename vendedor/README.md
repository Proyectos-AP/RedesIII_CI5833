# Aplicación web del vendedor

En este directorio se define la aplicación web correspondiente al sitio de comercio del vendedor. 

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
4. Agregar como variable de ambiente el valor de la llave secreta para usar el captcha de Google. Para ello, abrir el archivo 
~/.bashrc y agregar la siguiente línea
``` bash
  export CAPTCHA_SECRET_KEY=<clave_secreta>
```
  donde *clave_secreta* se encuentra en la carpeta Drive del proyecto.

# Ejecución

1. Activar el ambiente virtual
``` bash
  source bin/env/activate
```

2. Ejecutar el servidor de *Django*
``` python
  python manage.py runserver
```

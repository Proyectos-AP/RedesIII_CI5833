# Banco del cliente

## Instalación

### Crear un ambiente virtual con `venv`
```bash
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Crear la BD.
```bash
python manage.py migrate
```

### Popular la BD.
Ejecutar la app según dice *Ejecución*, ir a `http://<ip>:<puerto>/crearCuenta` y llenar el formulario.

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
4. Agrear el archivo de configuración llamado `config.json` dentro de `bancoCliente/private/`. Éste se encuentra en la carpeta Drive del proyecto.

# Ejecución
```bash
python manage.py runserver <ip>:<puerto>
```

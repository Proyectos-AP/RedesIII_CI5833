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

# Ejecución
```bash
python manage.py runserver <ip>:<puerto>
```

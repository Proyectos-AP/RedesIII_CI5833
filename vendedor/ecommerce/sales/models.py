from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=20,decimal_places=2)
    vendor = models.CharField(max_length=10,default="")

# La interfaz solo permite comprar un producto a la vez.
class Receipt(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    # amount_payed = models.DecimalField(max_digits=20,decimal_places=2)

# Preguntas de seguridad
class Preguntas(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
	pregunta  = models.CharField(max_length=128, default="")
	respuesta = models.CharField(max_length=152, default="")

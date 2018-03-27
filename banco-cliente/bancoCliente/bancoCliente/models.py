from django.db import models

# Create your models here.
class Cuentas(models.Model):
	ci                = models.IntegerField(unique=True,default=0)
	tdc_number        = models.CharField(max_length=152, unique=True)
	secret_number     = models.CharField(max_length=152, default="")
	fecha_vencimiento = models.CharField(max_length=152, default="")
	saldo             = models.DecimalField(max_digits=20, decimal_places=2)

class Preguntas(models.Model):
	pregunta  = models.CharField(max_length=128, default="")
	respuesta = models.CharField(max_length=152, default="")
	cuenta    = models.ForeignKey(Cuentas, on_delete=models.CASCADE)
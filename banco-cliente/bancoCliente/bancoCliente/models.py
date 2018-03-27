from django.db import models

# Create your models here.
class Cuentas(models.Model):
	tdc_number = models.IntegerField(null=False,unique=True)
	saldo      = models.DecimalField(max_digits=20, decimal_places=2)

class Preguntas(models.Model):
	pregunta  = models.CharField(max_length=128, default="")
	respuesta = models.CharField(max_length=128, default="")
	cuenta    = models.ForeignKey(Cuentas, on_delete=models.CASCADE)
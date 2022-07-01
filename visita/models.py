from django.db import models
from estacionamiento.models import Parking

# Create your models here.

class Visita(models.Model):
    parking = models.ForeignKey(Parking,on_delete=models.CASCADE)
    
    nombre = models.CharField(max_length=100, null=True , blank=True , verbose_name='Nombre')
    correo = models.EmailField(max_length=100, null=True , blank=True , verbose_name='Correo')
    telefono = models.CharField(max_length=50, null=True, blank=True, verbose_name='Telefono')
    motivo = models.CharField(max_length=280, null=True , blank=True , verbose_name='Motivo')
    
    vehiculo=models.CharField(null=True,blank=True,max_length=30)
    matricula=models.CharField(null=True,blank=True,max_length=10)

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural= 'Visitas'
        ordering = ['nombre']

    def __str__(self):
     return (self.nombre)
   

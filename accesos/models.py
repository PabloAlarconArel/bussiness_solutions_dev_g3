from django.db import models
import datetime

from piso.models import Piso
from estacionamiento.models import Parking

# Create your models here.


class Ingreso(models.Model):
    parking = models.ForeignKey(Parking,on_delete=models.CASCADE)
    tipo = models.CharField(null=True, blank=True, max_length=30)
    matricula = models.CharField(null=True, blank=True, max_length=10) 
    vehiculo = models.CharField(null=True, blank=True, max_length=30)
    piso = models.ForeignKey(Piso, on_delete=models.CASCADE)
    estado = models.CharField(max_length=100, null=True,blank=True, default='Activo', verbose_name='Estado')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creada')
    caducidad = models.DateTimeField(auto_now_add=True, verbose_name='Horario Salida')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha Actualización')
    nombre = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre')
    motivo = models.CharField(max_length=100, null=True, blank=True, verbose_name='Motivo')
    telefono = models.IntegerField(null=True, blank=True, verbose_name='Telefono')
    class Meta:
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'


    def __str__(self):
        return str(self.matricula)

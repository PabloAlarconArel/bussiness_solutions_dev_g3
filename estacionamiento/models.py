from django.db import models
from piso.models import Piso

# Create your models here.

class Estacionamiento(models.Model):
    piso = models.ForeignKey(Piso,on_delete=models.CASCADE)
    nombre = models.CharField(null=True,blank=True,max_length=1)
    vip = models.IntegerField(null=True,blank=True)
    colaborador = models.IntegerField(null=True,blank=True)
    discapacitado = models.IntegerField(null=True,blank=True)
    visita = models.IntegerField(null=True,blank=True)
    capacidad = models.IntegerField(null=True,blank=True)

    status = models.CharField(max_length=100, null=True, blank=True, default='Activo', verbose_name='Estado')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha Actualización')

    class Meta:
        verbose_name = 'Estacionamiento'
        verbose_name_plural= 'Estacionamientos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Parking(models.Model):
    estacionamiento = models.ForeignKey(Estacionamiento,on_delete=models.CASCADE)
    lugar=models.IntegerField(null=True,blank=True)
    tipo=models.CharField(null=True,blank=True,max_length=30) #Vip/Colaborador/Discapacitado/Visita
    disponibilidad = models.CharField(max_length=100, null=True, blank=True, default='Desocupado', verbose_name='Disponibilidad')
    status = models.CharField(max_length=100, null=True, blank=True, default='Activo', verbose_name='Estado')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha Creación')
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha Actualización')

    class Meta:
        verbose_name = 'Parking'
        verbose_name_plural= 'Parkings'
        ordering = ['lugar']

    def __str__(self):
        return str(self.lugar)



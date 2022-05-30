from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import Group, User #importa los modelos Group y user
from sucursales.models import Sucursal
# Create your models here.
class Piso(models.Model):
    sucursal = models.ForeignKey(Sucursal,on_delete=CASCADE)
    nombre_piso = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre Del Piso')
    num_piso = models.IntegerField(null=True, blank=True, verbose_name='Numero Piso')
    tipo = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tipo Piso')
    estado = models.CharField(max_length=100, null=True, blank=True, default='Activo', verbose_name='Estado')   
    created = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    updated = models.DateTimeField(auto_now=True,verbose_name='Fecha Actualización')
    class Meta:
        verbose_name = 'Piso'
        verbose_name_plural = 'Pisos'
        ordering = ['num_piso']   
    def __str__(self):
        return self.num_piso
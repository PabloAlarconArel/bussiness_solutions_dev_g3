from django.db import models
from django.contrib.auth.models import Group, User #importa los modelos Group y user

class Salas(models.Model):
    sucursal_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='Id de sucursal')
    nombre = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre sala')
    tipo = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tipo sala')
    Numero_piso = models.CharField(max_length=100, null=True, blank=True, verbose_name='Numero de piso')
    estado = models.CharField(max_length=100, null=True, blank=True, default='Activo', verbose_name='Estado')   
    created = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    updated = models.DateTimeField(auto_now=True,verbose_name='Fecha Actualización')
    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'
        ordering = ['sala_nombre']   
    def __str__(self):
        return self.nombre
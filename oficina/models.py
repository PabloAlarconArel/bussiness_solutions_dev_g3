from django.db import models
from django.contrib.auth.models import Group, User #importa los modelos Group y user
# Create your models here.

class Oficina(models.Model):
    piso_id = models.CharField(max_length=100, null=True, blank=True, verbose_name='Id de oficina')
    nombre = models.CharField(max_length=100, null=True, blank=True, verbose_name='nombre oficina')
    capacidad = models.IntegerField(null=True, blank=True, verbose_name='Capacidad de la oficna')
    estado = models.CharField(max_length=100, null=True, blank=True, default='Activo', verbose_name='Estado')   
    created = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    updated = models.DateTimeField(auto_now=True,verbose_name='Fecha Actualización')
    class Meta:
        verbose_name = 'oficina'
        verbose_name_plural = 'oficinas'
        ordering = ['nombre']   
    def __str__(self):
        return self.nombre
from django.db import models
from django.contrib.auth.models import Group, User #importa los modelos Group y user
# Create your models here.

class Oficina(models.Model):
    oficina_nombre = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre oficina')
    tipo = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tipo oficina')
    piso_oficina = models.IntegerField(null=True, blank=True, verbose_name='Piso donde esta la oficina')
    estado = models.CharField(max_length=100, null=True, blank=True, default='Activo', verbose_name='Estado')   
    created = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    updated = models.DateTimeField(auto_now=True,verbose_name='Fecha Actualización')
    class Meta:
        verbose_name = 'oficina'
        verbose_name_plural = 'oficinas'
        ordering = ['oficina_nombre']   
    def __str__(self):
        return self.oficina_nombre
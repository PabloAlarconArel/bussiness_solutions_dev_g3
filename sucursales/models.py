from django.db import models
from django.contrib.auth.models import Group, User #importa los modelos Group y user
# Create your models here.

class Sucursal(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre Sucursal')
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='Direccion Sucursal')
    contact = models.CharField(max_length=20, null=True, blank=True, verbose_name='Contacto Sucursal')
    email = models.EmailField(max_length=254)
    created = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    updated = models.DateTimeField(auto_now=True,verbose_name='Fecha Actualización')
    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering = ['name']   
    def __str__(self):
        return self.name
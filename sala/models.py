from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import Group, User #importa los modelos Group y user
from piso.models import Piso

class Sala(models.Model):
    piso = models.ForeignKey(Piso,on_delete=CASCADE) 
    nombre_sala_r = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre sala de reunion')
    capacidad_sala_r = models.IntegerField(null=True, default=0, blank=True, verbose_name='Capacidad')
    estado = models.CharField(max_length=100, null=True, blank=True, default='Activo', verbose_name='Estado')   
    created = models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    updated = models.DateTimeField(auto_now=True,verbose_name='Fecha Actualización')
    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'
        ordering = ['nombre_sala_r']   
    def __str__(self):
        return self.nombre_sala_r
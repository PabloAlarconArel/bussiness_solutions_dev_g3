import json
from django.db.models import Count, Avg, Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from sala.models import Salas
from piso.models import Piso

# Create your views here.

@api_view(['POST'])
def salas_sala_add_rest(request, format=None):    
    if request.method == 'POST':
        piso = request.data['piso_id']
        nombre_sala_r = request.data['nombre_sala_r'] 
        capacidad_sala_r = request.data['capacidad_sala_r'] 
        estado = request.data['estado']
        piso = Piso.objects.get(pk = piso)
        if nombre_sala_r == '' or estado == '' or capacidad_sala_r == '' or piso == '':
            return Response({'Msj': "Error los datos no pueder estar en blanco"})                         
        sala_save = Salas(
            nombre_sala_r = nombre_sala_r,
            capacidad_sala_r = capacidad_sala_r,
            estado = estado,
            piso = piso,
            )
        sala_save.save()
        return Response({'Msj': "Sala de reuniones creada"})
    else:
        return Response({'Msj': "Error método no soportado"})


@api_view(['GET'])
def salas_sala_list_rest(request, format=None):    
    if request.method == 'GET':
        sala_list =  Salas.objects.all().order_by('nombre_sala_r')
        sala_json = []
        for s in sala_list:
            sala_json.append({'piso':s.piso_id, 'Sala':s.nombre_sala_r, 'capacidad':s.capacidad_sala_r, 'estado':s.estado})
        return Response({'Listado': sala_json})
    else:
        return Response({'Msj': "Error método no soportado"})


@api_view(['POST'])
def salas_sala_update_element_rest(request, format=None):
    if request.method == 'POST':
        sala_id = request.data['sala_id']
        nombre_sala_r= request.data['nombre_sala_r']
        capacidad_sala_r = request.data['capacidad_sala_r']
        estado = request.data['estado']
        Salas.objects.filter(pk = sala_id).update(nombre_sala_r = nombre_sala_r)
        Salas.objects.filter(pk = sala_id ).update(capacidad_sala_r = capacidad_sala_r)
        Salas.objects.filter(pk = sala_id ).update(estado = estado)
        return Response({'Msj' : 'sala editada con éxito'})    
    else:
        return Response({'Msj' : 'Error método no soportado'})


@api_view(['POST'])
def salas_sala_get_element_rest(request, format=None):
     if request.method == 'POST':
        sala_json = []
        sala_id = request.data['sala_id']
        sala_array = Salas.objects.get(pk = sala_id)
        sala_json.append(
            {
                'id': sala_array.id,
                'nombre_sala_r': sala_array.nombre_sala_r,
                'capacidad_sala_r': sala_array.capacidad_sala_r,
                'estado': sala_array.estado})
        return Response({ sala_array.nombre_sala_r:sala_json })
     else:
        return Response({'Msj':"Error método no soportado"})
        

@api_view(['POST'])
def salas_sala_del_element_rest(request,format=None):
    if request.method =='POST':
        sala_id=request.data['sala_id']
        Salas.objects.filter(pk = sala_id).delete()
        return Response({'Msj':'Sala de reuniones eliminadad exitosamente'})
    else:
        return Response({'Msj':'Error método no soportado'})
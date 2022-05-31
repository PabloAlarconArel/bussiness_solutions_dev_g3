import json
from django.db.models import Count, Avg, Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from oficina.models import Oficina
from piso.models import Piso

# Create your views here.
@api_view(['POST'])
def oficinas_oficina_add_rest(request, format=None):
    if request.method == 'POST':
        piso = request.data['piso_id']
        nombre_oficina = request.data['nombre_oficina'] 
        capacidad_oficina = request.data['capacidad_oficina']
        try:
            piso = Piso.objects.get(pk = piso)
            if nombre_oficina == ''or capacidad_oficina == '' or piso == '':
                return Response({'Msj': "Error los datos no pueder estar en blanco"})
            if not isinstance(capacidad_oficina, int):
                return  Response({'Msj': "Error capacidad solo acepta numeros enteros"})
            oficina_save = Oficina(
                    nombre_oficina = nombre_oficina,
                    capacidad_oficina = capacidad_oficina,
                    piso = piso, 
                    )
            oficina_save.save()
            return Response({'Msj': "La oficina ha sido creada exitosamente"})
        except Piso.DoesNotExist:
            return Response({'Msj': "Error el id de piso no existe"}) 
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['GET'])
def oficinas_oficina_list_rest(request, format=None):    
    if request.method == 'GET':
        oficina_list =  Oficina.objects.all().order_by('nombre_oficina')
        oficina_json = []
        for o in oficina_list:
            oficina_json.append({'Piso':o.piso_id, 'Oficina':o.nombre_oficina,'Capacidad Oficina':o.capacidad_oficina,'Estado':o.estado,})
        return Response({'Listado': oficina_json})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def oficinas_oficina_update_element_rest(request, format=None):
    if request.method == 'POST':
        nombre_oficina = request.data['nombre_oficina']
        oficina_id = request.data['oficina_id']
        capacidad_oficina =request.data ['capacidad_oficina']
        estado =request.data ['estado']
        Oficina.objects.filter(pk = oficina_id ).update(nombre_oficina = nombre_oficina)
        Oficina.objects.filter(pk = oficina_id ).update(capacidad_oficina = capacidad_oficina)
        Oficina.objects.filter(pk = oficina_id ).update(estado = estado)
        if not isinstance(capacidad_oficina, int):
            return  Response({'Msj': "Error capacidad solo acepta numeros enteros"})
        return Response({'Msj' : 'Oficina actualizada con éxito'})    
    else:
        return Response({'Msj' : 'Error método no soportado'})

@api_view(['POST'])
def oficinas_oficina_get_element_rest(request, format=None):
    if request.method == 'POST':
        oficina_json = []
        oficina_id = request.data['oficina_id']
        oficina_array = Oficina.objects.get(pk = oficina_id)
        oficina_json.append(
            {
                'ID': oficina_array.id,
                'Piso ID': oficina_array.piso_id,
                'Nombre Oficina': oficina_array.nombre_oficina,
                'Capacidad Oficina': oficina_array.capacidad_oficina,
                'Estado': oficina_array.estado})
        return Response({ oficina_array.nombre_oficina:oficina_json })

@api_view(['POST'])
def oficinas_oficina_del_element_rest(request,format=None):
    if request.method =='POST':
        oficina_id=request.data['oficina_id']
        Oficina.objects.filter(pk = oficina_id).delete()
        return Response({'Msj':'La oficina ha sido eliminadad exitosamente'})
    else:
        return Response({'Msj':'Error método no soportado'})


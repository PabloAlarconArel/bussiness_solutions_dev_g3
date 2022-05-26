import json
from django.db.models import Count, Avg, Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from sala.models import Salas

# Create your views here.


@api_view(['GET'])
def sala_sala_list_rest(request, format=None):    
    if request.method == 'GET':
        sala_list =  Salas.objects.all().order_by('name')
        sala_json = []
        for s in sala_list:
            sala_json.append({'Sala':s.name, 'capacidad':s.capacidad})
        return Response({'Listado': sala_json})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def sala_salas_update_element_rest(request, format=None):
    if request.method == 'POST':
        id_piso = request.data['id_piso']
        name= request.data['name']
        capacidad= request.data['capacidad']
        Salas.objects.filter(pk = id_piso).update(capacidad = capacidad)
        Salas.objects.filter(pk = id_piso ).update(name = name)
        return Response({'Msj' : 'sala editada con éxito'})    
    else:
        return Response({'Msj' : 'Error método no soportado'})


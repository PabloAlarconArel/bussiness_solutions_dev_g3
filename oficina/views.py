import json
from django.db.models import Count, Avg, Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from oficina.models import Oficina

# Create your views here.

@api_view(['GET'])
def oficina_oficina_list_rest(request, format=None):    
    if request.method == 'GET':
        oficina_list =  Oficina.objects.all().order_by('name')
        oficina_json = []
        for s in oficina_list:
            oficina_json.append({'Sala':s.name,'capacidad':s.capacidad,})
        return Response({'Listado': oficina_json})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def oficina_oficina_update_element_rest(request, format=None):
    if request.method == 'POST':
        id_piso = request.data['id_piso ']
        name = request.data['name']
        capacidad =capacidad.data ['capacidad']
        Oficina.objects.filter(pk = id_piso ).update(name = name)
        Oficina.objects.filter(pk = id_piso ).update(capacidad = capacidad)
        return Response({'Msj' : 'oficina editada con éxito'})    
    else:
        return Response({'Msj' : 'Error método no soportado'})


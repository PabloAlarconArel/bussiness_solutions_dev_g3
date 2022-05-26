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
        sala_list =  Salas.objects.all().order_by('nombre')
        sala_json = []
        for s in sala_list:
            sala_json.append({'Sala':s.nombre,'tipo':s.tipo,'numero_piso':s.numero_piso})
        return Response({'Listado': sala_json})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def sala_salas_update_element_rest(request, format=None):
    if request.method == 'POST':
        sucursal_id = request.data['sucursal_id']
        nombre= request.data['nombre']
        tipo = request.data['address']
        numero_piso = request.data['contact']
        email = request.data['email']
        Salas.objects.filter(pk = sucursal_id).update(tipo = tipo)
        Salas.objects.filter(pk = sucursal_id).update(email = email)
        Salas.objects.filter(pk = sucursal_id).update(nombre = nombre)
        Salas.objects.filter(pk = sucursal_id).update(numero_piso = numero_piso)
        return Response({'Msj' : 'Sucursal editada con éxito'})    
    else:
        return Response({'Msj' : 'Error método no soportado'})


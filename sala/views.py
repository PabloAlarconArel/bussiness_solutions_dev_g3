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
def sala_salas_list_contains(request, format=None):    
    if request.method == 'GET':
        sala_list =  Salas.objects.all().order_by('name')
        sala_json = []
        for s in sala_list:
            sala_json.append({'sala':s.name,'Email':s.email,'Direccion':s.address,'Contacto':s.contact})
        return Response({'Listado': sala_json})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def sala_salas_update_element_rest(request, format=None):
    if request.method == 'POST':
        Salas_id = request.data['sala_id']
        name = request.data['name']
        address = request.data['address']
        contact = request.data['contact']
        email = request.data['email']
        Salas.objects.filter(pk = Salas_id).update(address = address)
        Salas.objects.filter(pk = Salas_id).update(email = email)
        Salas.objects.filter(pk = Salas_id).update(name = name)
        Salas.objects.filter(pk = Salas_id).update(contact = contact)
        return Response({'Msj' : 'Sucursal editada con éxito'})    
    else:
        return Response({'Msj' : 'Error método no soportado'})


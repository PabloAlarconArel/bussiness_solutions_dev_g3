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

@api_view(['POST'])
def oficina_oficina_list_contains(request, format=None):
    if request.method == 'POST':
        search = request.data['search']
        oficina_list_count = Oficina.objects.filter(Q(name__icontains=search)|Q(address__icontains=search)).count()
        if oficina_list_count > 0:
            oficina_list =   Oficina.objects.filter(Q(name__icontains=search)|Q(address__icontains=search)).order_by('name')
            oficina_json = []
            for h in oficina_list:
                oficina_json.append({'oficina':h.name,'address':h.address})
            return Response({'Listado': oficina_json})
        else:
            return Response({'Msj': 'No existen habilidades que concuerden en estado o nombre con la cadena '+str(search)})
    else:
        return Response({'Msj': 'Error método no soportado'})

@api_view(['POST'])
def oficina_oficina_update_element_rest(request, format=None):
    if request.method == 'POST':
        oficina_id = request.data['sucursal_id']
        name = request.data['name']
        address = request.data['address']
        contact = request.data['contact']
        email = request.data['email']
        Oficina.objects.filter(pk = oficina_id).update(address = address)
        Oficina.objects.filter(pk = oficina_id).update(email = email)
        Oficina.objects.filter(pk = oficina_id).update(name = name)
        Oficina.objects.filter(pk = oficina_id).update(contact = contact)
        return Response({'Msj' : 'oficina editada con éxito'})    
    else:
        return Response({'Msj' : 'Error método no soportado'})


import json
from django.db.models import Count, Avg, Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from sucursales.models import Sucursal

# Create your views here.

@api_view(['POST'])
def sucursales_sucursal_add_rest(request, format=None):    
    if request.method == 'POST':
        name = request.data['name'] 
        email = request.data['email'] 
        contact = request.data['contact']
        address = request.data['address']
        if name == '' or email == '':
            return Response({'Msj': "Error los datos no pueder estar en blanco"})                         
        sucursal_save = Sucursal(
            name = name,
            email = email,
            contact = contact,
            address = address,
            )
        sucursal_save.save()
        return Response({'Msj': "Sucursal creada"})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['GET'])
def sucursales_sucursal_list_rest(request, format=None):    
    if request.method == 'GET':
        sucursal_list =  Sucursal.objects.all().order_by('name')
        sucursal_json = []
        for s in sucursal_list:
            sucursal_json.append({'Sucursal':s.name,'Email':s.email,'Direccion':s.address,'Contacto':s.contact})
        return Response({'Listado': sucursal_json})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def sucursales_sucursal_list_contains(request, format=None):
    if request.method == 'POST':
        search = request.data['search']
        sucursal_list_count = Sucursal.objects.filter(Q(name__icontains=search)|Q(address__icontains=search)).count()
        if sucursal_list_count > 0:
            sucursal_list =   Sucursal.objects.filter(Q(name__icontains=search)|Q(address__icontains=search)).order_by('name')
            sucursal_json = []
            for h in sucursal_list:
                sucursal_json.append({'Sucursal':h.name,'address':h.address})
            return Response({'Listado': sucursal_json})
        else:
            return Response({'Msj': 'No existen habilidades que concuerden en estado o nombre con la cadena '+str(search)})
    else:
        return Response({'Msj': 'Error método no soportado'})

@api_view(['POST'])
def sucursales_sucursal_update_element_rest(request, format=None):
    if request.method == 'POST':
        sucursal_id = request.data['sucursal_id']
        name = request.data['name']
        address = request.data['address']
        contact = request.data['contact']
        email = request.data['email']
        Sucursal.objects.filter(pk = sucursal_id).update(address = address)
        Sucursal.objects.filter(pk = sucursal_id).update(email = email)
        Sucursal.objects.filter(pk = sucursal_id).update(name = name)
        Sucursal.objects.filter(pk = sucursal_id).update(contact = contact)
        return Response({'Msj' : 'Sucursal editada con éxito'})    
    else:
        return Response({'Msj' : 'Error método no soportado'})

@api_view(['POST'])
def sucursales_sucursal_del_element_rest(request,format=None):
    if request.method =='POST':
        sucursal_id=request.data['sucursal_id']
        Sucursal.objects.filter(pk = sucursal_id).delete()
        return Response({'Msj':'Sucursal eliminadad exitosamente'})
    else:
        return Response({'Msj':'Error método no soportado'})

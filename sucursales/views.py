import json
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
        estado = request.data['estado'] 
        contact = request.data['contact']
        address = request.data['address']
        if name == '' or estado == '':
            return Response({'Msj': "Error los datos no pueder estar en blanco"})                         
        sucursal_save = Sucursal(
            name = name,
            estado = estado,
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
            sucursal_json.append({'Sucursal':s.name,'Estado':s.estado,'Direccion':s.address,'Contacto':s.contact})
        return Response({'Listado': sucursal_json})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def sucursales_sucursal_get_element_rest(request, format=None):
     if request.method == 'POST':
        sucursal_json = []
        sucursal_id = request.data['sucursal_id']
        sucursal_array = Sucursal.objects.get(pk = sucursal_id)
        sucursal_json.append(
            {
                'id': sucursal_array.id,
                'name': sucursal_array.name,
                'address': sucursal_array.address,
                'contact': sucursal_array.contact,
                'estado': sucursal_array.estado})
        return Response({ sucursal_array.name:sucursal_json })
     else:
        return Response({'Msj':"Error método no soportado"})

@api_view(['POST'])
def sucursales_sucursal_update_element_rest(request, format=None):
    if request.method == 'POST':
        sucursal_id = request.data['sucursal_id']
        name = request.data['name']
        address = request.data['address']
        contact = request.data['contact']
        estado = request.data['estado']
        Sucursal.objects.filter(pk = sucursal_id).update(address = address)
        Sucursal.objects.filter(pk = sucursal_id).update(estado = estado)
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

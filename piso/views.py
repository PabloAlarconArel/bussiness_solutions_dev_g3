import json
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from piso.models import Piso	

# Create your views here.
@api_view(['POST'])
def pisos_piso_add_rest(request, format=None):    
    if request.method == 'POST':
        nombre_piso = request.data['nombre_piso']
        num_piso = request.data['num_piso'] 
        tipo = request.data['tipo'] 
        if num_piso == '' or tipo == '' or nombre_piso == '':
            return Response({'Msj': "Error los datos no pueder estar en blanco"})                         
        piso_save = Piso(
            nombre_piso = nombre_piso,
            num_piso = num_piso,
            tipo = tipo,
            )
        piso_save.save()
        return Response({'Msj': "Piso creado exitosamente"})
    else:
        return Response({'Msj': "Error método no soportado"})   

@api_view(['GET'])
def pisos_piso_list_rest(request, format=None):    
    if request.method == 'GET':
        piso_list =  Piso.objects.all().order_by('num_piso')
        piso_json = []
        for p in piso_list:
            piso_json.append({'Numero de piso':p.num_piso,'Nombre Del Piso':p.nombre_piso,'tipo':p.tipo,})
        return Response({'Listado': piso_json})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def pisos_piso_update_element_rest(request, format=None):
    if request.method == 'POST':
        nombre_piso = request.data['nombre_piso']
        piso_id = request.data['piso_id']
        num_piso = request.data['num_piso']
        tipo = request.data['tipo']
        estado = request.data['estado']
        Piso.objects.filter(pk = piso_id).update(num_piso = num_piso)
        Piso.objects.filter(pk = piso_id).update(estado = estado)
        Piso.objects.filter(pk = piso_id).update(tipo = tipo)
        Piso.objects.filter(pk = piso_id).update(nombre_piso = nombre_piso)
        return Response({'Msj' : 'Piso editado con éxito'})    
    else:
        return Response({'Msj' : 'Error método no soportado'})

@api_view(['POST'])
def pisos_piso_get_element_rest(request, format=None):
    if request.method == 'POST':
        piso_json = []
        piso_id = request.data['piso_id']
        piso_array = Piso.objects.get(pk = piso_id)
        piso_json.append(
            {
                'id': piso_array.id,
                'nombre_piso': piso_array.nombre_piso,
                'num_piso': piso_array.num_piso,
                'tipo': piso_array.tipo,
                'estado': piso_array.estado})
        return Response({ piso_array.num_piso:piso_json })
    else:
        return Response({'Msj':"Error método no soportado"})

@api_view(['POST'])
def pisos_piso_del_element_rest(request,format=None):
    if request.method =='POST':
        piso_id=request.data['piso_id']
        Piso.objects.filter(pk = piso_id).delete()
        return Response({'Msj':'Piso eliminado con éxito'})
    else:
        return Response({'Msj':'Error método no soportado'})


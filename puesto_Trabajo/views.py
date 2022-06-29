import json
from django.db.models import Count, Avg, Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from puesto_Trabajo.models import Puesto
from piso.models import Piso


@api_view(['POST'])
def puesto_trabajo_puesto_add_rest(request, format=None):    
    if request.method == 'POST':
        piso = request.data['piso_id']
        nombre_puesto_r = request.data['nombre_puesto_r'] 
        capacidad_puesto_r = request.data['capacidad_puesto_r'] 
        try:
            piso = Piso.objects.get(pk = piso)
            if nombre_puesto_r == '' or capacidad_puesto_r == '' or piso == '':
                return Response({'Msj': "Error los datos no pueder estar en blanco"})   
            if not isinstance(capacidad_puesto_r, int):
                return  Response({'Msj': "Error capacidad solo acepta numeros enteros"})                    
            puesto_save = Puesto(
                nombre_puesto_r = nombre_puesto_r,
                capacidad_puesto_r = capacidad_puesto_r,
                piso = piso,
                )
            puesto_save.save()
            return Response({'Msj': "Puesto de trabajo creada exitosamente"})
        except Piso.DoesNotExist:
            return Response({'Msj': "Error el id de piso no existe"})  
    else:
        return Response({'Msj': "Error método no soportado"})


@api_view(['GET'])
def puesto_trabajo_puesto_list_rest(request, format=None):    
    if request.method == 'GET':
        puesto_list =  Puesto.objects.all().order_by('nombre_puesto_r')
        puesto_json = []
        for s in puesto_list:
            puesto_json.append({'Piso':s.piso_id, 'Puesto':s.nombre_puesto_r, 'Capacidad':s.capacidad_puesto_r, 'Estado':s.estado})
        return Response({'Listado Puestos': puesto_json})
    else:
        return Response({'Msj': "Error método no soportado"})


@api_view(['POST'])
def puesto_trabajo_puesto_update_element_rest(request, format=None):
    if request.method == 'POST':
        puesto_id = request.data['puesto_id']
        nombre_puesto_r= request.data['nombre_puesto_r']
        capacidad_puesto_r = request.data['capacidad_puesto_r']
        estado = request.data['estado']
        Puesto.objects.filter(pk = puesto_id).update(nombre_puesto_r = nombre_puesto_r)
        Puesto.objects.filter(pk = puesto_id ).update(capacidad_puesto_r = capacidad_puesto_r)
        Puesto.objects.filter(pk = puesto_id ).update(estado = estado)
        if not isinstance(capacidad_puesto_r, int):
            return  Response({'Msj': "Error capacidad solo acepta numeros enteros"})  
        return Response({'Msj' : 'Puesto de trabajo actualizada con éxito'})    
    else:
        return Response({'Msj' : 'Error método no soportado'})


@api_view(['POST'])
def puesto_trabajo_puesto_get_element_rest(request, format=None):
     if request.method == 'POST':
        puesto_json = []
        puesto_id = request.data['puesto_id']
        puesto_array = Puesto.objects.get(pk = puesto_id)
        puesto_json.append(
            {
                'ID': puesto_array.id,
                'Piso ID': puesto_array.piso_id,
                'Nombre Puesto de Trabajo': puesto_array.nombre_puesto_r,
                'Capacidad Puesto de trabajo': puesto_array.capacidad_puesto_r,
                'Estado': puesto_array.estado})
        return Response({ puesto_array.nombre_puesto_r:puesto_json })
     else:
        return Response({'Msj':"Error método no soportado"})
        

@api_view(['POST'])
def puesto_trabajo_puesto_del_element_rest(request,format=None):
    if request.method =='POST':
        puesto_id=request.data['puesto_id']
        Puesto.objects.filter(pk = puesto_id).delete()
        return Response({'Msj':'Puesto de trabajo eliminada exitosamente'})
    else:
        return Response({'Msj':'Error método no soportado'})
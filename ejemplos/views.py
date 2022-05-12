import json
from django.db.models import Count, Avg, Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (
	api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from ejemplos.models import Habilidad, Heroe 

#rest crea habilidad
@api_view(['POST'])
def ejemplos_habilidad_add_rest(request, format=None):    
    if request.method == 'POST':
        nombre = request.data['nombre'] 
        nivel = request.data['nivel'] 
        if nombre == '' or nivel == '':
            return Response({'Msj': "Error los datos no pueder estar en blanco"})                         
        habilidad_save = Habilidad(
            nombre = nombre,
            nivel = nivel,
            )
        habilidad_save.save()
        return Response({'Msj': "Habilidad creada"})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['GET'])
def ejemplos_habilidad_list_rest(request, format=None):    
    if request.method == 'GET':
        habilidad_list =  Habilidad.objects.all().order_by('nombre')
        habilidad_json = []
        for h in habilidad_list:
            habilidad_json.append({'habilidad':h.nombre,'nivel':h.nivel,'estado':h.estado})
        return Response({'Listado': habilidad_json})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def ejemplos_habilidad_get_element_rest(request, format=None):    
    if request.method == 'POST':
        habilidad_json = []
        habilidad_id = request.data['habilidad_id']
        habilidad_array =  Habilidad.objects.get(pk=habilidad_id)
        habilidad_json.append(
            {'id':habilidad_array.id,
             'nombre':habilidad_array.nombre,
             'nivel':habilidad_array.nivel,
             'estado':habilidad_array.estado})
        return Response({habilidad_array.nombre:habilidad_json})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def ejemplos_habilidad_update_element_rest(request, format=None):    
    if request.method == 'POST':
        habilidad_id = request.data['habilidad_id']
        nombre = request.data['nombre']
        nivel = request.data['nivel']
        estado = request.data['estado']
        Habilidad.objects.filter(pk=habilidad_id).update(nombre=nombre)
        Habilidad.objects.filter(pk=habilidad_id).update(nivel=nivel)
        Habilidad.objects.filter(pk=habilidad_id).update(estado=estado)
        return Response({'Msj':'Habilidad editada con éxito'})
    else:
        return Response({'Msj': 'Error método no soportado'})

@api_view(['POST'])
def ejemplos_habilidad_del_element_rest(request, format=None):    
    if request.method == 'POST':
        habilidad_id = request.data['habilidad_id']
        Habilidad.objects.filter(pk=habilidad_id).delete()
        return Response({'Msj':'Habilidad eliminada con éxito'})
    else:
        return Response({'Msj': 'Error método no soportado'})

@api_view(['POST'])
def ejemplos_habilidad_list_date_rest(request, format=None):    
    if request.method == 'POST':
        created = request.data['created']
        habilidad_list_count = Habilidad.objects.filter(created=created).count()
        if habilidad_list_count > 0:
            habilidad_list =  Habilidad.objects.filter(created=created).order_by('nombre')
            habilidad_json = []
            for h in habilidad_list:
                habilidad_json.append({'habilidad':h.nombre,'nivel':h.nivel,'estado':h.estado})
            return Response({'Listado': habilidad_json})
        else:
            return Response({'Msj': 'No existen habilidades creadas el '+str(created)})
    else:
        return Response({'Msj': 'Error método no soportado'})

@api_view(['POST'])
def ejemplos_habilidad_list_range_date_rest(request, format=None):    
    if request.method == 'POST':
        initial = request.data['initial']
        final = request.data['final']
        habilidad_list_count = Habilidad.objects.filter(created__range=(initial,final)).count()
        if habilidad_list_count > 0:
            habilidad_list =  Habilidad.objects.filter(created__range=(initial,final)).order_by('nombre')
            habilidad_json = []
            for h in habilidad_list:
                habilidad_json.append({'habilidad':h.nombre,'nivel':h.nivel,'estado':h.estado})
            return Response({'Listado': habilidad_json})
        else:
            return Response({'Msj': 'No existen habilidades creadas entre el '+str(initial)+' al '+str(final)})
    else:
        return Response({'Msj': 'Error método no soportado'})


@api_view(['POST'])
def ejemplos_habilidad_list_contains(request, format=None):    
    if request.method == 'POST':
        search = request.data['search']
        habilidad_list_count = Habilidad.objects.filter(Q(nombre__icontains=search)|Q(estado__icontains=search)).count()
        if habilidad_list_count > 0:
            habilidad_list =  Habilidad.objects.filter(Q(nombre__icontains=search)|Q(estado__icontains=search)).order_by('nombre')
            habilidad_json = []
            for h in habilidad_list:
                habilidad_json.append({'habilidad':h.nombre,'nivel':h.nivel,'estado':h.estado})
            return Response({'Listado': habilidad_json})
        else:
            return Response({'Msj': 'No existen habilidades que concuerden en estado o nombre con la cadena '+str(search)})    
    else:
        return Response({'Msj': 'Error método no soportado'})
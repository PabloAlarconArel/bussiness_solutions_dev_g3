from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
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

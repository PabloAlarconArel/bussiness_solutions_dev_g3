from audioop import add
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (
	api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from branches.models import Branch

#rest crea habilidad
@api_view(['POST'])
def branches_branch_add_rest(request, format=None):    
    if request.method == 'POST':
        name = request.data['name'] 
        email = request.data['email'] 
        contact = request.data['contact']
        address = request.data['address']
        if name == '' or email == '':
            return Response({'Msj': "Error los datos no pueder estar en blanco"})                         
        branch_save = Branch(
            name = name,
            email = email,
            contact = contact,
            address = address,
            )
        branch_save.save()
        return Response({'Msj': "Sucursal creada"})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['GET'])
def branches_branch_list_rest(request, format=None):    
    if request.method == 'GET':
        branch_list =  Branch.objects.all().order_by('name')
        branch_json = []
        for s in branch_list:
            branch_json.append({'Sucursal':s.name,'Email':s.email,'Direccion':s.address,'Contacto':s.contact})
        return Response({'Listado': branch_json})
    else:
        return Response({'Msj': "Error método no soportado"})

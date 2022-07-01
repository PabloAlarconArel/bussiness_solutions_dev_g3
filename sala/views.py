#from asyncio.windows_events import NULL
import json
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from registration.models import Profile
from django.db.models import Count, Avg, Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from sala.models import Sala
from piso.models import Piso


# Create your views here.

@login_required
def salas_main(request):
    profile = Profile.objects.get(user_id = request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'salas/salas_main.html'
    return render(request, template_name, {'profile':profile , 'template_name': 'salas/salas_main.html'})


@login_required
def salas_sala_add(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'salas/salas_add.html'
    return render(request, template_name, {'profile':profile , 'template_name': 'salas/salas_main.html'})


@login_required
def salas_sala_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        piso_id = request.POST.get('piso_id')
        nombre_sala_r = request.POST.get('nombre_sala_r')        
        capacidad_sala_r = request.POST.get('capacidad_sala_r')     
        piso = Piso.objects.get(pk = piso_id)
        if nombre_sala_r == '' or capacidad_sala_r == '' or piso == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('salas_sala_add')
        sala_save = Sala(
            nombre_sala_r = nombre_sala_r,
            capacidad_sala_r = capacidad_sala_r,
            piso = piso,
            )
        sala_save.save()
        messages.add_message(request, messages.INFO, 'Sala creada con éxito')
        return redirect('salas_list_salas')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

@login_required
def salas_sala_ver(request,sala_id):
    profile = Profile.objects.get(user_id = request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    sala_data = Sala.objects.get(pk=sala_id)
    template_name = 'salas/salas_sala_ver.html'
    return render(request, template_name, {'profile':profile, 'sala_data':sala_data , 'template_name': 'salas/salas_main.html'})

@login_required
def salas_list_salas(request, page = None, search = None):
    profile = Profile.objects.get(user_id = request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if page == None:
        page = request.GET.get('page')
    else:
        page = page
    if request.GET.get('page') == None:
        page = page
    else:
        page = request.GET.get('page') 
    if search == None:
        search = request.GET.get('search')
    else:
        search = search
    if request.GET.get('search') == None:
        search = search
    else:
        search = request.GET.get('search') 
    if request.method == 'POST':
        search = request.POST.get('search') 
        page = None
    s_list = []
    if search == None or search == "None":
        s_count = Sala.objects.filter(estado='Activo').count()
        s_list_array = Sala.objects.filter(estado='Activo').order_by('nombre_sala_r')
        for s in s_list_array:
            s_list.append({'id':s.id, 'piso_id':s.piso_id, 'nombre_sala_r':s.nombre_sala_r, 'capacidad_sala_r':s.capacidad_sala_r, 'estado':s.estado})
    else:
        s_count = Sala.objects.filter(estado='Activo').filter(nombre_sala_r__icontains=search).count()
        s_list_array = Sala.objects.filter(estado='Activo').filter(nombre_sala_r__icontains=search).order_by('nombre_sala_r')
        for s in s_list_array:
            s_list.append({'id':s.id, 'piso_id':s.piso_id, 'nombre_sala_r':s.nombre_sala_r, 'capacidad_sala_r':s.capacidad_sala_r, 'estado':s.estado})            
    paginator = Paginator(s_list, 1) 
    s_list_paginate = paginator.get_page(page)   
    template_name = 'salas/salas_list_salas.html'
    return render(request,template_name, {'template_name':template_name,'s_list_paginate':s_list_paginate,'paginator':paginator,'page':page})

#Endpoints

@api_view(['POST'])
def salas_sala_add_rest(request, format=None):    
    if request.method == 'POST':
        piso = request.data['piso_id']
        nombre_sala_r = request.data['nombre_sala_r'] 
        capacidad_sala_r = request.data['capacidad_sala_r'] 
        try:
            piso = Piso.objects.get(pk = piso)
            if nombre_sala_r == '' or capacidad_sala_r == '' or piso == '':
                return Response({'Msj': "Error los datos no pueder estar en blanco"})   
            if not isinstance(capacidad_sala_r, int):
                return  Response({'Msj': "Error capacidad solo acepta numeros enteros"})                    
            sala_save = Sala(
                nombre_sala_r = nombre_sala_r,
                capacidad_sala_r = capacidad_sala_r,
                piso = piso,
                )
            sala_save.save()
            return Response({'Msj': "Sala de reuniones creada exitosamente"})
        except Piso.DoesNotExist:
            return Response({'Msj': "Error el id de piso no existe"})  
    else:
        return Response({'Msj': "Error método no soportado"})


@api_view(['GET'])
def salas_sala_list_rest(request, format=None):    
    if request.method == 'GET':
        sala_list =  Sala.objects.all().order_by('nombre_sala_r')
        sala_json = []
        for s in sala_list:
            sala_json.append({'Piso':s.piso_id, 'Sala':s.nombre_sala_r, 'Capacidad':s.capacidad_sala_r, 'Estado':s.estado})
        return Response({'Listado Salas': sala_json})
    else:
        return Response({'Msj': "Error método no soportado"})


@api_view(['POST'])
def salas_sala_update_element_rest(request, format=None):
    if request.method == 'POST':
        sala_id = request.data['sala_id']
        nombre_sala_r = request.data['nombre_sala_r']
        capacidad_sala_r = request.data['capacidad_sala_r']
        estado = request.data['estado']
        Sala.objects.filter(pk = sala_id).update(nombre_sala_r = nombre_sala_r)
        Sala.objects.filter(pk = sala_id ).update(capacidad_sala_r = capacidad_sala_r)
        Sala.objects.filter(pk = sala_id ).update(estado = estado)
        if not isinstance(capacidad_sala_r, int):
            return  Response({'Msj': "Error capacidad solo acepta numeros enteros"})  
        return Response({'Msj' : 'Sala actualizada con éxito'})    
    else:
        return Response({'Msj' : 'Error método no soportado'})


@api_view(['POST'])
def salas_sala_get_element_rest(request, format=None):
     if request.method == 'POST':
        sala_json = []
        sala_id = request.data['sala_id']
        sala_array = Sala.objects.get(pk = sala_id)
        sala_json.append(
            {
                'ID': sala_array.id,
                'Piso ID': sala_array.piso_id,
                'Nombre Sala': sala_array.nombre_sala_r,
                'Capacidad Sala': sala_array.capacidad_sala_r,
                'Estado': sala_array.estado
            })
        return Response({ sala_array.nombre_sala_r:sala_json })
     else:
        return Response({'Msj':"Error método no soportado"})
        

@api_view(['POST'])
def salas_sala_del_element_rest(request,format=None):
    if request.method == 'POST':
        sala_id = request.data['sala_id']
        Sala.objects.filter(pk = sala_id).delete()
        return Response({'Msj':'Sala de reuniones eliminadad exitosamente'})
    else:
        return Response({'Msj':'Error método no soportado'})
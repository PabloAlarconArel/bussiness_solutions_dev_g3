from asyncio.windows_events import NULL
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
from oficina.models import Oficina
from piso.models import Piso


@login_required
def oficinas_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'oficinas/oficinas_main.html'
    return render(request,template_name,{'profile':profile})


@login_required
def oficinas_oficina_add(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'oficinas/oficinas_add.html'
    return render(request,template_name,{'profile':profile})


@login_required
def oficinas_oficina_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        piso_id = request.POST.get('piso_id')
        nombre_oficina = request.POST.get('nombre_oficina')        
        capacidad_oficina = request.POST.get('capacidad_oficina')     
        piso = Piso.objects.get(pk = piso_id)
        if nombre_oficina == '' or capacidad_oficina == '' or piso == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('oficinas_oficina_add')
        oficina_save = Oficina(
            nombre_oficina = nombre_oficina,
            capacidad_oficina = capacidad_oficina,
            piso = piso,
            )
        oficina_save.save()
        messages.add_message(request, messages.INFO, 'Oficina creada con éxito')
        return redirect('oficinas_list_oficinas')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

@login_required
def oficinas_oficina_ver(request,oficina_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    oficina_data = Oficina.objects.get(pk=oficina_id)
    template_name = 'oficinas/oficinas_oficina_ver.html'
    return render(request,template_name,{'profile':profile,'oficina_data':oficina_data})

@login_required
def oficinas_list_oficinas(request,page=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)
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
    o_list = []
    if search == None or search == "None":
        o_count = Oficina.objects.filter(estado='Activo').count()
        o_list_array = Oficina.objects.filter(estado='Activo').order_by('nombre_oficina')
        for o in o_list_array:
            o_list.append({'id':o.id,'piso_id':o.piso_id, 'nombre_oficina':o.nombre_oficina,'capacidad_oficina':o.capacidad_oficina, 'estado':o.estado})
    else:
        o_count = Oficina.objects.filter(estado='Activo').filter(nombre_oficina__icontains=search).count()
        o_list_array = Oficina.objects.filter(estado='Activo').filter(nombre_oficina__icontains=search).order_by('nombre_oficina')
        for o in o_list_array:
            o_list.append({'id':o.id,'piso_id':o.piso_id,'nombre_oficina':o.nombre_oficina,'capacidad_oficina':o.capacidad_oficina,'estado':o.estado})            
    paginator = Paginator(o_list, 1) 
    o_list_paginate= paginator.get_page(page)   
    template_name = 'oficinas/oficinas_list_oficinas.html'
    return render(request,template_name,{'template_name':template_name,'o_list_paginate':o_list_paginate,'paginator':paginator,'page':page})




#Endpoints.
@api_view(['POST'])
def oficinas_oficina_add_rest(request, format=None):
    if request.method == 'POST':
        piso = request.data['piso_id']
        nombre_oficina = request.data['nombre_oficina'] 
        capacidad_oficina = request.data['capacidad_oficina']
        try:
            piso = Piso.objects.get(pk = piso)
            if nombre_oficina == ''or capacidad_oficina == '' or piso == '':
                return Response({'Msj': "Error los datos no pueder estar en blanco"})
            if not isinstance(capacidad_oficina, int):
                return  Response({'Msj': "Error capacidad solo acepta numeros enteros"})
            oficina_save = Oficina(
                    nombre_oficina = nombre_oficina,
                    capacidad_oficina = capacidad_oficina,
                    piso = piso, 
                    )
            oficina_save.save()
            return Response({'Msj': "La oficina ha sido creada exitosamente"})
        except Piso.DoesNotExist:
            return Response({'Msj': "Error el id de piso no existe"}) 
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['GET'])
def oficinas_oficina_list_rest(request, format=None):    
    if request.method == 'GET':
        oficina_list =  Oficina.objects.all().order_by('nombre_oficina')
        oficina_json = []
        for o in oficina_list:
            oficina_json.append({'Piso':o.piso_id, 'Oficina':o.nombre_oficina,'Capacidad Oficina':o.capacidad_oficina,'Estado':o.estado,})
        return Response({'Listado': oficina_json})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def oficinas_oficina_update_element_rest(request, format=None):
    if request.method == 'POST':
        nombre_oficina = request.data['nombre_oficina']
        oficina_id = request.data['oficina_id']
        capacidad_oficina =request.data ['capacidad_oficina']
        estado =request.data ['estado']
        Oficina.objects.filter(pk = oficina_id ).update(nombre_oficina = nombre_oficina)
        Oficina.objects.filter(pk = oficina_id ).update(capacidad_oficina = capacidad_oficina)
        Oficina.objects.filter(pk = oficina_id ).update(estado = estado)
        if not isinstance(capacidad_oficina, int):
            return  Response({'Msj': "Error capacidad solo acepta numeros enteros"})
        return Response({'Msj' : 'Oficina actualizada con éxito'})    
    else:
        return Response({'Msj' : 'Error método no soportado'})

@api_view(['POST'])
def oficinas_oficina_get_element_rest(request, format=None):
    if request.method == 'POST':
        oficina_json = []
        oficina_id = request.data['oficina_id']
        oficina_array = Oficina.objects.get(pk = oficina_id)
        oficina_json.append(
            {
                'ID': oficina_array.id,
                'Piso ID': oficina_array.piso_id,
                'Nombre Oficina': oficina_array.nombre_oficina,
                'Capacidad Oficina': oficina_array.capacidad_oficina,
                'Estado': oficina_array.estado})
        return Response({ oficina_array.nombre_oficina:oficina_json })

@api_view(['POST'])
def oficinas_oficina_del_element_rest(request,format=None):
    if request.method =='POST':
        oficina_id=request.data['oficina_id']
        Oficina.objects.filter(pk = oficina_id).delete()
        return Response({'Msj':'La oficina ha sido eliminadad exitosamente'})
    else:
        return Response({'Msj':'Error método no soportado'})


import json
#nuevas importaciones 30-05-2022
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from registration.models import Profile
#fin nuevas importaciones 30-05-2022

from django.db.models import Count, Avg, Q
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (
	api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from piso.models import Piso
from puesto_Trabajo.models import Puesto

@login_required
def puesto_Trabajo_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'puesto_Trabajo/puesto_Trabajo_main.html'
    return render(request,template_name,{'profile':profile})

@login_required
def puesto_Trabajo_puesto_add(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'puesto_Trabajo/puesto_Trabajo_add.html'
    return render(request,template_name,{'profile':profile})

@login_required
def puesto_Trabajo_puesto_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        nombre_puesto = request.POST.get('nombre puesto')
        capacidad_puesto = request.POST.get('capacidad puesto') 
        estado = request.POST.get('estado')    
        if nombre_puesto == '' or capacidad_puesto == '' or estado == '' :
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('puesto_Trabajo_puesto_add')
        puesto_save = Puesto(
            nombre_puesto = nombre_puesto,
            capacidad_puesto = capacidad_puesto,
            estado = estado
            )
        puesto_save.save()
        messages.add_message(request, messages.INFO, 'Puesto de Trabajo ingresado con éxito')
        return redirect('puesto_Trabajo_list_puesto_Trabajo')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

@login_required
def puesto_Trabajo_puesto_ver(request,puesto_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    puesto_data = Puesto.objects.get(pk=puesto_id)
    template_name = 'puesto_Trabajo/puesto_Trabajo_puesto_ver.html'
    return render(request,template_name,{'profile':profile,'puesto_data':puesto_data})

@login_required
def Puesto_Trabajo_list_puesto_Trabajo(request,page=None,search=None):
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
    h_list = []
    if search == None or search == "None":
        h_count = Puesto.objects.count()
        h_list_array = Puesto.objects.order_by('name')
        for h in h_list_array:
            h_list.append({'id':h.id,'puesto_trabajo':h.puesto_trabajo,'estado':h.estado, 'capacidad_puesto':h.capacidad_puesto})
    else:
        h_count =  Puesto.objects.filter(name__icontains=search).count()
        h_list_array = Puesto.objects.filter(name__icontains=search).order_by('name')
        for h in h_list_array:
            h_list.append({'id':h.id,'puesto_trabajo':h.puesto_trabajo,'estado':h.estado, 'capacidad_puesto':h.capacidad_puesto})        
    paginator = Paginator(h_list, 1) 
    h_list_paginate= paginator.get_page(page)   
    template_name = 'Puesto_Trabajo/Puesto_Trabajo_list_puesto_Trabajo.html'
    return render(request,template_name,{'template_name':template_name,'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page})


@api_view(['POST'])
def puesto_trabajo_puesto_add_rest(request, format=None):    
    if request.method == 'POST':
        piso = request.data['piso_id']
        nombre_puesto= request.data['nombre_puesto'] 
        capacidad_puesto= request.data['capacidad_puesto'] 
        try:
            piso = Piso.objects.get(pk = piso)
            if nombre_puesto == '' or capacidad_puesto == '' or piso == '':
                return Response({'Msj': "Error los datos no pueder estar en blanco"})   
            if not isinstance(capacidad_puesto, int):
                return  Response({'Msj': "Error capacidad solo acepta numeros enteros"})                    
            puesto_save = Puesto(
                nombre_puesto_ = nombre_puesto,
                capacidad_puesto_ = capacidad_puesto,
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
            puesto_json.append({'Piso':s.piso_id, 'Puesto':s.nombre_puesto, 'Capacidad':s.capacidad_puesto, 'Estado':s.estado})
        return Response({'Listado Puestos': puesto_json})
    else:
        return Response({'Msj': "Error método no soportado"})


@api_view(['POST'])
def puesto_trabajo_puesto_update_element_rest(request, format=None):
    if request.method == 'POST':
        puesto_id = request.data['puesto_id']
        nombre_puesto= request.data['nombre_puesto']
        capacidad_puesto = request.data['capacidad_puesto']
        estado = request.data['estado']
        Puesto.objects.filter(pk = puesto_id).update(nombre_puesto= nombre_puesto)
        Puesto.objects.filter(pk = puesto_id ).update(capacidad_puesto = capacidad_puesto)
        Puesto.objects.filter(pk = puesto_id ).update(estado = estado)
        if not isinstance(capacidad_puesto, int):
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
                'Nombre Puesto de Trabajo': puesto_array.nombre_puesto,
                'Capacidad Puesto de trabajo': puesto_array.capacidad_puesto,
                'Estado': puesto_array.estado})
        return Response({ puesto_array.nombre_puesto:puesto_json })
     else:
        return Response({'Msj':"Error método no soportado"})
        

@api_view(['POST'])
def puesto_trabajo_puesto_del_element_rest(request,format=None):
    if request.method =='POST':
        puesto_id=request.data['puesto_id']
        Puesto.objects.filter(pk = puesto_id).delete()
        return Response({'Msj':'Puesto de trabajo eliminado exitosamente'})
    else:
        return Response({'Msj':'Error método no soportado'})
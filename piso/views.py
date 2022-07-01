import json
import re
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
from sucursales.models import Sucursal

# TEmplates

@login_required
def pisos_piso_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'piso/pisos_main.html'
    return render(request,template_name,{'profile':profile, 'template_name': 'piso/pisos_main.html'})

@login_required
def pisos_piso_add(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'piso/pisos_add.html'
    return render(request,template_name,{'profile':profile, 'template_name': 'piso/pisos_main.html'})

@login_required
def pisos_piso_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        sucursal = request.POST.get('sucursal_id')
        nombre_piso = request.POST.get('nombre_piso')
        num_piso = request.POST.get('num_piso')
        tipo = request.POST.get('tipo')
        sucursal = Sucursal.objects.get(pk = sucursal) 
        if num_piso == '' or tipo == '' or nombre_piso == '' or sucursal =='':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('pisos_piso_add')
        piso_save = Piso(
            nombre_piso = nombre_piso,
            num_piso = num_piso,
            tipo = tipo,
            sucursal = sucursal,
            )
        piso_save.save()
        messages.add_message(request, messages.INFO, 'Sucursal ingresada con éxito')
        return redirect('pisos_list_piso')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')


@login_required
def pisos_list_piso(request,page=None,search=None):
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
        h_count = Piso.objects.count()
        h_list_array = Piso.objects.order_by('id')
        for h in h_list_array:
            h_list.append({'id':h.id,'sucursal_id':h.sucursal_id,'num_piso':h.num_piso,'nombre_piso':h.nombre_piso,'tipo':h.tipo, 'estado':h.estado})
    else:
        h_count = Piso.objects.filter(num_piso__icontains=search).count()
        h_list_array = Piso.objects.filter(num_piso__icontains=search).order_by('num_piso')
        for h in h_list_array:
            h_list.append({'id':h.id,'sucursal_id':h.sucursal_id,'num_piso':h.num_piso,'nombre_piso':h.nombre_piso,'tipo':h.tipo, 'estado':h.estado})         
    paginator = Paginator(h_list, 10) 
    h_list_paginate= paginator.get_page(page)   
    template_name = 'piso/pisos_list.html'
    return render(request,template_name,{'template_name':template_name,'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'search':search, 'template_name': 'piso/pisos_main.html'})

@login_required
def pisos_piso_ver(request,id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    piso_data = Piso.objects.get(pk=id)
    template_name = 'piso/pisos_ver.html'
    return render(request,template_name,{'profile':profile,'piso_data':piso_data, 'template_name': 'piso/pisos_main.html'})

@login_required
def pisos_piso_update(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        piso_id = request.POST['id']
        nombre_piso = request.POST['nombre_piso']
        sucursal_id = request.POST['sucursal_id']
        num_piso = request.POST['num_piso']
        tipo = request.POST['tipo']
        estado = request.POST['estado']
        Piso.objects.filter(pk = piso_id).update(num_piso = num_piso)
        Piso.objects.filter(pk = piso_id).update(estado = estado)
        Piso.objects.filter(pk = piso_id).update(tipo = tipo)
        Piso.objects.filter(pk = piso_id).update(nombre_piso = nombre_piso)
        messages.add_message(request, messages.INFO, 'Piso actualizado con éxito')
        return redirect('pisos_list_piso')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

@login_required
def pisos_piso_delete(request, id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    Piso.objects.get(pk=id).delete()
    messages.add_message(request, messages.INFO, 'Piso eliminado con éxito')
    return redirect('pisos_list_piso')


# Create your views here.
@api_view(['POST'])
def pisos_piso_add_rest(request, format=None):    
    if request.method == 'POST':
        sucursal = request.data['sucursal_id']
        nombre_piso = request.data['nombre_piso']
        num_piso = request.data['num_piso'] 
        tipo = request.data['tipo']
        sucursal = Sucursal.objects.get(pk = sucursal) 
        if isinstance(nombre_piso,int):
            return Response({'Msj': "Error los datos son invalidos"})
        if not isinstance(num_piso,int):
            return Response({'Msj': "Error los datos son invalidos"})
        if isinstance(tipo,int):
            return Response({'Msj': "Error los datos son invalidos"})
        if nombre_piso.isspace() or tipo.isspace():
            return Response({'Msj': "Error los datos no pueden ser espacios"})
        if num_piso == '' or tipo == '' or nombre_piso == '' or sucursal =='':
            return Response({'Msj': "Error los datos no pueder estar en blanco"})                         
        piso_save = Piso(
            nombre_piso = nombre_piso,
            num_piso = num_piso,
            tipo = tipo,
            sucursal = sucursal,
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
            piso_json.append({'sucursal':p.sucursal_id,'Numero de piso':p.num_piso,'Nombre Del Piso':p.nombre_piso,'tipo':p.tipo, 'estado':p.estado})
        return Response({'Listado': piso_json})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def pisos_piso_update_element_rest(request, format=None):
    if request.method == 'POST':
        try:
            nombre_piso = request.data['nombre_piso']
            piso_id = request.data['piso_id']
            piso_array = Piso.objects.get(pk = piso_id) 
            num_piso = request.data['num_piso']
            tipo = request.data['tipo']
            estado = request.data['estado']
            if not isinstance(piso_id,int):
                return Response({'Msj': "Error los datos son invalidos"})
            if nombre_piso.isspace() or tipo.isspace() or estado.isspace():
                return Response({'Msj': "Error los datos no pueden ser espacios"})
            if nombre_piso == '' or piso_id == '' or num_piso == '' or tipo == '' or  estado =='':
                return Response({'Msj': "Error los datos no pueder estar en blanco"})    
            if piso_array:
                Piso.objects.filter(pk = piso_id).update(num_piso = num_piso)
                Piso.objects.filter(pk = piso_id).update(estado = estado)
                Piso.objects.filter(pk = piso_id).update(tipo = tipo)
                Piso.objects.filter(pk = piso_id).update(nombre_piso = nombre_piso)
                return Response({'Msj' : 'Piso editado con éxito'})  
        except Piso.DoesNotExist:
            return Response({'Msj' : 'No existe este piso'})
        except ValueError:
            return Response({'Msj' : 'Valor no soportado'})
    else:
        return Response({'Msj' : 'Error método no soportado'})

@api_view(['POST'])
def pisos_piso_get_element_rest(request, format=None):
    if request.method == 'POST':
        try:
            piso_json = []
            piso_id = request.data['piso_id']
            piso_array = Piso.objects.get(pk = piso_id)
            if not isinstance(piso_id,int):
                return Response({'Msj': "Error los datos son invalidos"})
            if piso_array:
                piso_json.append(
                    {
                        'id': piso_array.id,
                        'nombre_piso': piso_array.nombre_piso,
                        'num_piso': piso_array.num_piso,
                        'tipo': piso_array.tipo,
                        'estado': piso_array.estado})
                return Response({ piso_array.num_piso:piso_json })
        except Piso.DoesNotExist:
            return Response({'Msj' : 'No existe este piso'})
        except ValueError:
            return Response({'Msj' : 'Valor no soportado'})
    else:
        return Response({'Msj':"Error método no soportado"})

@api_view(['POST'])
def pisos_piso_del_element_rest(request,format=None):
    if request.method =='POST':
        try:
            piso_id=request.data['piso_id']
            piso_array = Piso.objects.get(pk = piso_id)
            if not isinstance(piso_id,int):
                return Response({'Msj': "Error los datos son invalidos"})
            if piso_array: 
                Piso.objects.filter(pk = piso_id).delete()
                return Response({'Msj':'Piso eliminado con éxito'})
        except Piso.DoesNotExist:
            return Response({'Msj' : 'No existe este piso'})
        except ValueError:
            return Response({'Msj' : 'Valor no soportado'})
    else:
        return Response({'Msj':'Error método no soportado'})


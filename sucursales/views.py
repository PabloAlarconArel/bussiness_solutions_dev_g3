from email.headerregistry import Address
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
from sucursales.models import Sucursal

@login_required
def sucursales_master_menu(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'sucursales/sucursales_master_menu.html'
    return render(request,template_name,{'profile':profile, 'template_name' : 'sucursales/sucursales_master_menu.html'})

@login_required
def sucursales_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'sucursales/sucursales_main.html'
    return render(request,template_name,{'profile':profile, 'template_name': 'sucursales/sucursales_main.html'})

@login_required
def sucursales_sucursal_add(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'sucursales/sucursales_add.html'
    return render(request,template_name,{'profile':profile, 'template_name': 'sucursales/sucursales_main.html'})

@login_required
def sucursales_sucursal_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        name = request.POST.get('nombre')
        address = request.POST.get('direccion')
        contact = request.POST.get('contacto')
        estado = request.POST.get('estado')
        if name == '' or address == '' or contact == '' or estado == '' :
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('sucursales_sucursal_add')
        sucursal_save = Sucursal(
            name = name,
            address = address,
            contact = contact,
            estado = estado
            )
        sucursal_save.save()
        messages.add_message(request, messages.INFO, 'Sucursal ingresada con éxito')
        return redirect('sucursales_list_sucursales')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

@login_required
def sucursales_sucursal_delete(request,sucursal_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    Sucursal.objects.get(pk=sucursal_id).delete()
    messages.add_message(request, messages.INFO, 'Sucursal borrada con éxito')
    return redirect('sucursales_list_sucursales')

@login_required
def sucursales_sucursal_update(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        sucursal_id=request.POST['id']
        name = request.POST['nombre']
        address = request.POST['direccion']
        contact= request.POST['contacto']
        estado = request.POST['estado']
        Sucursal.objects.filter(pk = sucursal_id).update(name = name)
        Sucursal.objects.filter(pk = sucursal_id).update(address=address)
        Sucursal.objects.filter(pk = sucursal_id).update(contact=contact)
        Sucursal.objects.filter(pk = sucursal_id).update(estado = estado)
        messages.add_message(request, messages.INFO, 'Sucursal ingresada con éxito')
        return redirect('sucursales_list_sucursales')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')       
@login_required
def sucursales_sucursal_ver(request,sucursal_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    sucursal_data = Sucursal.objects.get(pk=sucursal_id)
    template_name = 'sucursales/sucursales_sucursal_ver.html'
    return render(request,template_name,{'profile':profile,'sucursal_data':sucursal_data, 'template_name': 'sucursales/sucursales_main.html'})

@login_required
def sucursales_list_sucursales(request,page=None,search=None):
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
        h_count = Sucursal.objects.count()
        h_list_array = Sucursal.objects.order_by('name')
        for h in h_list_array:
            h_list.append({'id':h.id,'name':h.name,'estado':h.estado, 'contact':h.contact, 'address' :h.address})
    else:
        h_count = Sucursal.objects.filter(name__icontains=search).count()
        h_list_array = Sucursal.objects.filter(name__icontains=search).order_by('name')
        for h in h_list_array:
            h_list.append({'id':h.id,'name':h.name,'estado':h.estado, 'contact':h.contact, 'address' :h.address})         
    paginator = Paginator(h_list, 10) 
    h_list_paginate= paginator.get_page(page)   
    template_name = 'sucursales/sucursales_list_sucursales.html'
    return render(request,template_name,{'template_name':template_name,'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page, 'template_name': 'sucursales/sucursales_main.html'})

@api_view(['POST'])
def sucursales_sucursal_add_rest(request, format=None):    
    if request.method == 'POST':
        name = request.data['name'] 
        estado = request.data['estado'] 
        contact = request.data['contact']
        address = request.data['address']
        if isinstance(name,int):
            return Response({'Msj': "Error los datos son invalidos"})
        if isinstance(estado,int):
            return Response({'Msj': "Error los datos son invalidos"})
        if isinstance(contact,int):
            return Response({'Msj': "Error los datos son invalidos"})
        if isinstance(address,int):
            return Response({'Msj': "Error los datos son invalidos"})
        if name.isspace() or estado.isspace() or contact.isspace() or address.isspace():
            return Response({'Msj': "Error los datos no pueden ser espacios"})
        if name == '' or estado == '' or contact == '' or address == '':
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
        try:
            sucursal_list =  Sucursal.objects.all().order_by('name')
            sucursal_json = []
            for s in sucursal_list:
                sucursal_json.append({'Sucursal':s.name,'Estado':s.estado,'Direccion':s.address,'Contacto':s.contact})
            return Response({'Listado': sucursal_json})
        except Sucursal.DoesNotExist:
            return Response({'Msj' : 'No existe sucursal para listar'})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def sucursales_sucursal_get_element_rest(request, format=None):
     if request.method == 'POST':
        try: 
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
        except Sucursal.DoesNotExist:
            return Response({'Msj' : 'No existe sucursal para mostrar'})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
     else:
        return Response({'Msj':"Error método no soportado"})

@api_view(['POST'])
def sucursales_sucursal_update_element_rest(request, format=None):
    if request.method == 'POST':
        try:
            sucursal_id = request.data['sucursal_id']
            sucursal_array = Sucursal.objects.get(pk = sucursal_id)
            name = request.data['name']
            address = request.data['address']
            contact = request.data['contact']
            estado = request.data['estado']
            if isinstance(name,int):
                return Response({'Msj': "Error los datos son invalidos"})
            if isinstance(estado,int):
                return Response({'Msj': "Error los datos son invalidos"})
            if isinstance(contact,int):
                return Response({'Msj': "Error los datos son invalidos"})
            if isinstance(address,int):
                return Response({'Msj': "Error los datos son invalidos"})
            if name.isspace() or estado.isspace() or contact.isspace() or address.isspace():
                return Response({'Msj': "Error los datos no pueden ser espacios"})
            if name == '' or estado == '' or contact == '' or address == '':
                return Response({'Msj': "Error los datos no pueder estar en blanco"})
            if sucursal_array:
                Sucursal.objects.filter(pk = sucursal_id).update()
                Sucursal.objects.filter(pk = sucursal_id).update(address = address)
                Sucursal.objects.filter(pk = sucursal_id).update(estado = estado)
                Sucursal.objects.filter(pk = sucursal_id).update(name = name)
                Sucursal.objects.filter(pk = sucursal_id).update(contact = contact)
                return Response({'Msj' : 'Sucursal editada con éxito'})
        except Sucursal.DoesNotExist:
            return Response({'Msj' : 'No existe sucursal para editar'})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})    
    else:
        return Response({'Msj' : 'Error método no soportado'})

@api_view(['POST'])
def sucursales_sucursal_del_element_rest(request,format=None):
    if request.method =='POST':
        try:
            sucursal_id=request.data['sucursal_id']
            sucursal_array = Sucursal.objects.get(pk = sucursal_id)
            if sucursal_array:
                Sucursal.objects.filter(pk = sucursal_id).delete()
            return Response({'Msj':'Sucursal eliminada exitosamente'})
        except Sucursal.DoesNotExist:
            return Response({'Msj' : 'No existe sucursal para borrar'})
        except ValueError:
            return Response({'Msj':"Valor no soportado"}) 
    else:
        return Response({'Msj':'Error método no soportado'})




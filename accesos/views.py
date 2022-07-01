from email import message
from glob import glob
from http.client import ResponseNotReady
import profile
from re import template
import re
from sqlite3 import Time
from turtle import update
from webbrowser import get
from django.shortcuts import redirect, render

# Create your views here.
import json
from ast import Return
from urllib import response
from django.shortcuts import render
from bussiness_solutions_dev_g3.settings import LOGIN_REDIRECT_URL
from estacionamiento.models import Parking
from piso.models import Piso
from registration.models import Profile
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from accesos.models import Ingreso


# Create datos  
@api_view(['POST'])
def accesos_ingreso_add_rest(request, format=None):
        if request.method == 'POST':
            try:
                lugar = request.data['lugar']
                if isinstance(lugar, float):  
                    return Response({'Msj': "El valor debe ser un numero entero"})
                if lugar == '':
                    return Response({'MSJ': 'Error, los espacios no pueden estar vacios'})
                parking = Parking.objects.get(pk=lugar)
                disponibilidad=parking.disponibilidad
                id=parking.id
                if disponibilidad != "Desocupado":
                    return Response({'Msj':"No se pudo reservar, el lugar se encuentra ocupado"})
                tipo = request.data['tipo']        
                if tipo == "":
                    return Response({'Msj':  "Imposibilidad de reserva, favor ingrese un tipo valido"})
                matricula = request.data['matricula']
                if matricula == '':
                    return Response({'Msj': "La matricula no puede estar vacia"})
                nombre = request.data['nombre']
                if isinstance(nombre, int):
                    return Response({'MSJ': 'Error, el nombre debe contener letras, no numeros'})
                piso = request.data['piso']
                pisos_a = Piso.objects.get(num_piso=piso)
                motivo = request.data['motivo']
                if motivo == '':
                    return Response({'Msj': "Favor realize un motivo de su acceso"})
                vehiculo = request.data['vehiculo']
                telefono = request.data['telefono']  
                if isinstance(telefono, str):
                    return Response({'Msj': "El telefono solo pueden ser números"})
                ingreso_save = Ingreso(
                    tipo=tipo,
                    matricula=matricula,
                    nombre=nombre,
                    piso=pisos_a,
                    motivo=motivo,
                    vehiculo=vehiculo,
                    telefono=telefono,
                    parking=parking
                )
                ingreso_save.save()
                Parking.objects.filter(pk=id).update(disponibilidad="Ocupado")
                return Response({'Msj': "Acceso realizado"})
            except Parking.DoesNotExist:
                return Response({'Msj':"Error no hay ningun lugar con ese valor"})
        else:
            Response({'Msj': "Error método no soportado"})
#List Data
@api_view(['GET'])
def accesos_ingreso_list_rest(request, format=None):
    if request.method == 'GET':
        ingreso_list = Ingreso.objects.all()
        ingreso_json = []
        for a in ingreso_list:
            ingreso_json.append({
            'nombre':a.nombre,
            'tipo':a.tipo,
            'telefono':a.telefono,
            'vehiculo':a.vehiculo,
            'matricula':a.matricula,
            'motivo':a.motivo})
        return Response({'List':ingreso_json})
    else:
        return Response({'Msj':"Error método no soportado"})

#Read data for only lugar 
@api_view(['POST'])
def accesos_ingreso_get_element_rest(request,format=None):
    if request.method == 'POST':
        try:
            ingreso_id = request.data['lugar']
            ingreso_array_count = Ingreso.objects.filter(parking_id=ingreso_id).count()
            if  ingreso_array_count>0:
                ingreso_array=Ingreso.objects.filter(parking_id=ingreso_id)
                ingreso_json = []
            for h in ingreso_array:
                ingreso_json.append({'tipo': h.tipo,'motivo':h.motivo ,'vehiculo' :h.vehiculo, 'matricula': h.matricula , 'nombre':h.nombre})
            return Response({'lugar': ingreso_json})
        except Ingreso.DoesNotExist:
            return Response ({'MSJ': 'Error no hay coincidencias'})
        except ValueError:
            return Response ({'MSJ': 'Valor no soportado'})
    else:
        return Response({'Msj': "Error método no soportado"})
# Update data
@api_view(['POST'])
def accesos_ingreso_update_element_rest(request, format=None):
    if request.method == 'POST':
        try:    
                ingreso_id = request.data['lugar']
                nombre = request.data['nombre']
                if isinstance(nombre,int):
                    return Response ({'MSJ':'Error, el nombre solo debe ser letras'})
                tipo = request.data['tipo']
                if  tipo == '':
                    return Response ({'Msj':" Imposibilidad de Update  favor ingrese Tipos de usuario validos"})
                matricula = request.data['matricula']
                if matricula == '':
                    return Response ({'MSJ':'Error, debe ingresar una matricula'})
                telefono = request.data['telefono']
                if isinstance(telefono, str):
                    return Response({'Msj': "El telefono solo pueden ser números"})
                if telefono =='':
                    return Response ({'Msj' "El telefono no puede quedar vacio"})
                vehiculo = request.data['vehiculo']
                if vehiculo =='':
                    return Response ({'Msj' "El vehiculo no puede quedar vacio"})
                if nombre != '' and tipo != '' and matricula != '' and telefono != '' and vehiculo != '':
                    Ingreso.objects.filter(pk=ingreso_id).update(nombre=nombre)                             #NOMBRE TIPO ESTADO MATRICULA  TELEFONO CORREO AGREGAR
                    Ingreso.objects.filter(pk=ingreso_id).update(tipo=tipo)
                    Ingreso.objects.filter(pk=ingreso_id).update(matricula=matricula)
                    Ingreso.objects.filter(pk=ingreso_id).update(telefono=telefono)
                    Ingreso.objects.filter(pk=ingreso_id).update(vehiculo=vehiculo)
                    ingreso_json=[]
                    ingreso_array = Ingreso.objects.get(pk=ingreso_id)
                    ingreso_json.append({'id' : ingreso_array.id ,
                    'nombre' : ingreso_array.nombre,
                    'matricula' : ingreso_array.matricula,
                    'telefono' : ingreso_array.telefono,
                    'vehiculo' : ingreso_array.vehiculo ,
                    'tipo' : ingreso_array.tipo})
                    return Response({'Msj': "Update realizado con exito" , ingreso_array.nombre:ingreso_json})
        except Ingreso.DoesNotExist:
            return Response({'Msj':"Error no hay coincidencias"})
    else:
        return Response({'Msj': 'Error método no soportado'})
# Delete data
@api_view(['POST'])
def accesos_ingreso_del_element_rest(request, format=None):
    if request.method == 'POST':
        try:
            ingreso_id = request.data['lugar']
            ingreso_array = Ingreso.objects.get(pk=ingreso_id)
            id = ingreso_array.parking_id
            if ingreso_array:
                Ingreso.objects.filter(pk=ingreso_id).delete()
                Parking.objects.filter(pk=id).update(disponibilidad = "Desocupado")
                return Response({'Msj': 'Acceso eliminado con éxito'})
        except Ingreso.DoesNotExist:
            return Response({'Msj' : "Error no se encuentra la acceso registrada"})
        except ValueError:
                return Response({'Msj':"Favor ingrese un número valido de lugar"})
    else:
        return Response({'Msj': 'Error método no soportado'})
# Buscar por rango de fechas
@api_view(['POST'])
def accesos_ingreso_list_range_date_rest(request, format=None):
    if request.method == 'POST':
        initial = request.data['initial']

        final = request.data['final']

        ingreso_list_count = Ingreso.objects.filter(
            created__range=(initial, final)).count()
        if ingreso_list_count > 0:
            ingreso_list = Ingreso.objects.filter(
                created__range=(initial, final)).order_by('parking')
            ingreso_json = []
            for h in ingreso_list:
                ingreso_json.append(
                    {'tipo': h.tipo,'motivo':h.motivo ,'vehiculo' :h.vehiculo, 'matricula': h.matricula , 'nombre':h.nombre,'created': h.created, })
            return Response({'Listado': ingreso_json})
        else:
            return Response({'Msj': 'No existe un vehiculo asignado al rango de fechas entre  ' +str(initial) + '  al  '+str(final)})
    else:
        return Response({'Msj': 'Error, método no soportado'})
# Busca por registro de cadenas
@api_view(['POST'])
def accesos_ingreso_search_rest(request, format=None):
    if request.method == 'POST':
        try:
            search = request.data['search']
            if search != "":
                ingreso_list_count = Ingreso.objects.filter(nombre__icontains=search).count()
                if  ingreso_list_count > 0:
                    acceso_list = Ingreso.objects.filter(nombre__icontains=search)
                    acceso_json= []
                    for s in acceso_list:
                        acceso_json.append({'nombre':s.nombre,'vehiculo':s.vehiculo,'matricula':s.matricula})
                    return Response({'Listado':acceso_json})
                else:
                    return Response({'Msj':"No existen accesos que concuerden en estado o nombre con la cadena"})
            else: 
                return Response({'Msj':"No ha ingresado ningún valor para buscar"})
        except Ingreso.DoesNotExist:
            return Response({'Msj':"Error no hay coincidencias"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})
# Filtrar por tipo
@api_view(['POST'])
def accesos_ingreso_tipo_list_contains_rest(request, format=None):
    if request.method == 'POST':
        try:
            tipo = request.data['tipo']
            if  tipo== 'VIP' or tipo == 'Colaborador' or tipo == 'Discapacitado' or tipo == 'Visita'or tipo == 'visita'or tipo == 'discapacitado' or tipo == 'colaborador'  :
                tipos_count = Parking.objects.filter(tipo=tipo).count()
                if  tipos_count > 0:
                    tipos_list = Parking.objects.filter(tipo=tipo)
                    tipos_json= []
                    for i in tipos_list:
                        tipos_json.append({'lugar':i.lugar,'Estado':i.status,'Creado':i.created})
                    return Response({'Listado de ' + tipo :tipos_json})
                else:
                    return Response({'Msj':"No existen tipos que concuerden en estado o nombre con la cadena"})
            else: 
                return Response({'Msj':"Tipo no validoVIP|Colaborador|Discapacitado|Visita)"})
        except Ingreso.DoesNotExist:
            return Response({'Msj':"Error no hay coincidencias"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})
        
#########TEMPLATES##############
@login_required
def accesos_accesos_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'accesos/accesos_main.html'
    return render(request,template_name,{'profile':profile,'template_name': 'accesos/accesos_main.html'})

@login_required
def acceso_create_add(request, parking_id):
    profile=Profile.objects.get(user_id=request.user.id)
    parking_data = Parking.objects.get(pk=parking_id)
    if profile.group_id !=1:
        messages.add_message(request, messages.INFO , 'Intenta ingresar a un area para la que no tiene permisos')
        return redirect('chek_group_main')
    template_name = 'create_add.html'
    return render(request , template_name,{'profile' :profile , 'parking_data' :parking_data })
#Create Template
@login_required
def acceso_create_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id !=1:
        messages.add_message(request , messages.INFO , 'Intenta ingresar a un area para la que no tiene permisos')
        return redirect('chek_group_main')
    if request.method == 'POST':
        tipo= request.POST.get ('tipo')
        matricula=request.POST.get ('matricula')
        nombre=request.POST.get ('nombre')
        piso=request.POST.get ('piso')
        motivo=request.POST.get ('motivo')
        vehiculo=request.POST.get ('vehiculo')
        telefono=request.POST.get ('telefono')
        parking=request.POST.get ('parking')
        parking = Parking.objects.get(pk=parking)
        id = parking.id
        if tipo == '' or matricula == '' or nombre =='' or piso == '' or motivo == '' or vehiculo=='' or telefono=='' or parking=='':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('create_add.html')
        create_save = Ingreso(
        tipo=tipo,
        matricula=matricula,
        nombre=nombre,
        piso=piso,
        motivo=motivo,
        vehiculo=vehiculo,
        telefono=telefono,
        parking=parking
        )
        create_save.save()
        messages.add_message(request, messages.INFO, 'Acceso ingresado con éxito')
        Parking.objects.filter(pk=id).update(disponibilidad="Ocupado")
        return redirect('list_add.html')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')
        
        
        
@login_required
def acceso_ingreso_update(request , parking_id):
    profile = Profile.objects.get(user_id=request.user.id)
    parking_data = Parking.objects.get(pk=parking_id)
    acceso_data= Ingreso.objects.get(parking_id=parking_id)
    if profile.group_id != 1:
        message.add_message(request, messages.INFO, 'Intenta ingresar a un area para la que no tiene permisos')
        return redirect('chek_group_main')
    template_name = 'update_add.html'
    return render(request , template_name, {'profile' : profile , 'parking_data' : parking_data , 'acceso_data' : acceso_data})

#Update template
@login_required
def acceso_ingreso_update_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id !=1:
        messages.add_message(request , messages.INFO , 'Intenta ingresar a un area para la que no tiene permisos')
        return redirect('chek_group_main')
    if request.method == 'POST':
        nombre=request.POST.get ('nombre')
        tipo= request.POST.get ('tipo')
        matricula=request.POST.get ('matricula')
        vehiculo=request.POST.get ('vehiculo')
        telefono=request.POST.get ('telefono')
        parking=request.POST.get ('parking')
        acceso_data = Ingreso.objects.get(parking_id=parking)
        if tipo == '' or matricula == '' or nombre =='' or vehiculo=='' or telefono=='':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('create_add.html')
        Ingreso.objects.filter(pk=acceso_data).update(nombre=nombre)                             #NOMBRE TIPO ESTADO MATRICULA  TELEFONO CORREO AGREGAR
        Ingreso.objects.filter(pk=acceso_data).update(tipo=tipo)
        Ingreso.objects.filter(pk=acceso_data).update(matricula=matricula)
        Ingreso.objects.filter(pk=acceso_data).update(telefono=telefono)
        Ingreso.objects.filter(pk=acceso_data).update(vehiculo=vehiculo)
        messages.add_message(request , messages.INFO , 'Acceso actualizado con exito')
        return redirect ('list_add.html')
    else:
        message.add_message(request, message.INFO , 'Error en el método de envio')
        return redirect('chek_group_main')
#Delete template
@login_required
def acceso_ingreso_delete(request , parking_id):
    profile=Profile.objects.get(user_id = request.user.id)
    acceso_data=Ingreso.objects.get(parking_id=parking_id)
    if profile.group_id !=1:
        messages.add_message(request , messages.INFO , 'Intenta ingresar a un area para la que no tiene permisos')
        return redirect('chek_group_main')
    Ingreso.objects.filter(pk=acceso_data.id).delete()
    Parking.objects.filter(lugar=parking_id).update(disponibilidad = "Desocupado")
    messages.add_message(request , messages.INFO , 'Acceso eliminado con exito')
    return redirect ('list_add.html')
#Listar template
@login_required
def acceso_ingreso_list(request,page =None, search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id !=1:
        messages.add_message(request , messages.INFO ,  'Intenta ingresar a un area para la que no tiene permisos ')
        return redirect('chek_group_main')
    if page == None:
        page = request.GET.get
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
    a_list = []
    if search == None or search == 'None':
        a_count=Parking.objects.filter(status='Ocupado').count()
        orderbyList = [ 'lugar']
        a_list_array=Parking.objects.filter(status = 'Ocupado').order_by(*orderbyList)
        for a in a_list_array:
            ingreso=Ingreso.objects.get(pk=a.ingreso_id)
            a_list.append({'id': a.id , 'nombre' : a.nombre , 'tipo': a.tipo , 'motivo' : a.motivo , 'matricula' : a.matricula , 'telefono' : a.telefono ,'piso' : ingreso.piso, 'disponibilidad' : a.disponibilidad , 'vehiculo' :a.vehiculo})
    else:
        a_count=Parking.objects.filter(status='Ocupado').filter(lugar=search).count()
        orderbyList = ['lugar']
        a_list_array= a_list_array = Parking.objects.filter(status='Ocupado').filter(lugar=search).order_by(*orderbyList)
        for a in a_list_array:
            ingreso=Ingreso.objects.get(pk=a.ingreso_id)
            a_list.append({'id': a.id , 'nombre' : a.nombre , 'tipo': a.tipo , 'motivo' : a.motivo , 'matricula' : a.matricula , 'telefono' : a.telefono ,'piso' : ingreso.piso, 'disponibilidad' : a.disponibilidad , 'vehiculo' :a.vehiculo})
    paginator=Paginator(a_list, 2)
    a_list_paginate= paginator.get_page(page)   
    template_name = 'accesos/list_add.html'
    return render(request,template_name,{'template_name': 'accesos/accesos_main.html','a_list_paginate':a_list_paginate,'paginator':paginator,'page':page,'search':search})
@login_required
def acceso_ingreso_ver(request,parking_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    acceso_data= Ingreso.objects.get(pk=parking_id)
    template_name = 'read_add.html'
    return render(request,template_name,{'profile':profile,'acceso_data':acceso_data})

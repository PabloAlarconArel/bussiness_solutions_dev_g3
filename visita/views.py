from django.shortcuts import render,redirect
from estacionamiento.models import Parking
from piso.models import Piso
from sucursales.models import Sucursal
from visita.models import Visita
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
import re
from django.contrib.auth.decorators import login_required
from registration.models import Profile
from django.contrib import messages
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
from estacionamiento.models import Estacionamiento
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
@api_view(['POST'])
def visita_visita_add_rest(request, format=None):
    if request.method == 'POST':

            nombre=request.data['nombre']
            if nombre=="":
                return Response({'Msj':'El nombre no puede ir vacio'})
            correo=request.data['correo']
            if(re.search(regex,correo)):
                print()
            else:
                return Response({'Msj':'Email Invalido'})
            telefono=request.data['telefono']
            if telefono=="":
                return Response({'Msj':'Debe ingresar un numero de telefono'})
            motivo=request.data['motivo']
            if motivo=="":
                return Response({'Msj':'Debe ingresar el Motivo de la visita'})
            vehiculo=request.data['vehiculo']
            if vehiculo=="":
                return Response({'Msj':'No se permite vehiculo Vacia'})
            matricula=request.data['matricula']
            if matricula=="":
                return Response({'Msj':'No se permite Matricula Vacia'})

            parking = request.data['parking_id']
            parking = Parking.objects.get(pk=parking)
            
            disponibilidad= parking.disponibilidad
            tipo = parking.tipo
            id = parking.id

            if tipo != "Visita":
                return Response({'Msj':"No se pudo reservar, el tipo de estacionamiento seleccionado no es de visita"})

            if disponibilidad != "Desocupado":
                return Response({'Msj':"No se pudo reservar, el lugar se encuentra ocupado"})
            
            visita_save = Visita(
                nombre = nombre,
                correo = correo,
                telefono = telefono,
                motivo = motivo,
                vehiculo = vehiculo,
                matricula = matricula,
                parking = parking,
                )
            visita_save.save()
            Parking.objects.filter(pk=id).update(disponibilidad="Ocupado")
            return Response({'Msj':"Lugar Asignado"})
    else:
       return Response({'Msj': "Error método no soportado"})

@api_view(['GET'])
def visita_visita_list_rest(request, format=None):
    if request.method == 'GET':
        visita_list = Visita.objects.all()
        visita_json = []
        for es in visita_list:
            visita_json.append({'nombre':es.nombre,'correo':es.correo,'telefono':es.telefono,
            'vehiculo':es.vehiculo,'matricula':es.matricula,
            'motivo':es.motivo})
        return Response({'List':visita_json})
    else:
        return Response({'Msj':"Error método no soportado"})

@api_view(['POST'])
def visita_visita_update_element_rest(request, format=None):
    if request.method == 'POST':
        try:
            visita_id=request.data['visita_id']
            if isinstance(visita_id,(str,float)):
                return Response({'Msj':'visita_id invalido'})
            nombre= request.data['nombre']
            if isinstance(nombre,(int,float)):
                return Response({'Msj':'Nombre invalido'})
            correo = request.data['correo']
            if(re.search(regex,correo)):
                print()
            else:
                return Response({'Msj':'Email Invalido'})
            telefono = request.data['telefono']
            if isinstance(telefono,(str,float)):
                return Response({'Msj':'telefono invalido'})
            vehiculo = request.data['vehiculo']
            if isinstance(vehiculo,(str,float)):
                return Response({'Msj':'vehiculo invalido'})
            matricula = request.data['matricula']
            if isinstance(matricula,(int,float)):
                return Response({'Msj':'matricula invalida'})
            if nombre != '' and correo!='' and telefono!='' and vehiculo != '' and matricula!='':
                Visita.objects.filter(pk=visita_id).update(nombre=nombre)
                Visita.objects.filter(pk=visita_id).update(correo=correo)
                Visita.objects.filter(pk=visita_id).update(telefono=telefono) 
                Visita.objects.filter(pk=visita_id).update(vehiculo=vehiculo)
                Visita.objects.filter(pk=visita_id).update(matricula=matricula)
                visita_json=[]
                visita_array = Visita.objects.get(pk=visita_id)
                visita_json.append({'id':visita_array.id,'nombre':visita_array.nombre,'correo':visita_array.correo,'telefono':visita_array.telefono,'vehiculo': visita_array.vehiculo,'matricula':visita_array.matricula})
                return Response({'Msj':"Datos Actualizados",visita_array.nombre:visita_json}) 
            else:
                return Response({'Msj': "Error los datos no pueden estar en blanco"})
        except Visita.DoesNotExist:
            return Response({'Msj':"Error no hay coincidencias"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def visita_visita_delete_element_rest(request, format=None):
    if request.method == 'POST':
        try:
            visita_id = request.data['visita_id']
            if isinstance(visita_id,(str,float)):
                return Response({'Msj':'Id invalida'})
            visita_array = Visita.objects.get(pk=visita_id)
            parking = visita_array.parking_id
            if visita_array:
                Visita.objects.filter(pk=visita_id).delete()
                Parking.objects.filter(pk=parking).update(disponibilidad="Desocupado")
                return Response({'Msj':"Visita eliminada con exito"})
        except Visita.DoesNotExist:
            return Response({'Msj':"Error no hay coincidencias"})
        except Piso.DoesNotExist:
            return Response({'Msj':"Error no hay coincidencias"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})


@api_view(['POST'])
def visita_visita_search_rest(request, format=None):
    if request.method == 'POST':
        try:
            search = request.data['search']
            if search != "":
                visita_list_count = Visita.objects.filter(Q(nombre__icontains=search)|Q(correo__icontains=search)
                |Q(matricula__icontains=search)).count()
                if  visita_list_count > 0:
                    visita_list = Visita.objects.filter(Q(nombre__icontains=search)|Q(correo__icontains=search)
                    |Q(matricula__icontains=search))
                    visita_json= []
                    for s in visita_list:
                        visita_json.append({'nombre':s.nombre,'correo':s.correo,'vehiculo':s.vehiculo,
                        'matricula':s.matricula})
                    return Response({'Listado':visita_json})
                else:
                    return Response({'Msj':"No existen visitas que concuerden con la cadena de c"})
            else: 
                return Response({'Msj':"No ha ingresado ningún valor para buscar"})
        except Visita.DoesNotExist:
            return Response({'Msj':"No existe la visita"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})
    


#Templates
@login_required
def visita_visita_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'visita/visita_main.html'
    return render(request,template_name,{'profile':profile,'template_name':'visita/visita_main.html'})

@login_required
def visita_visita_add(request,estacionamiento_id,parking_id):
    profile = Profile.objects.get(user_id=request.user.id)
    parking_data = Parking.objects.get(pk=parking_id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    estacionamiento = Estacionamiento.objects.get(pk=estacionamiento_id)
    template_name = 'visita/visita_add.html'
    return render(request,template_name,{'profile':profile,'parking_data':parking_data,'estacionamiento':estacionamiento,'template_name':'visita/visita_main.html'})

@login_required
def visita_visita_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')     
        telefono = request.POST.get('telefono')
        motivo = request.POST.get('motivo')
        vehiculo = request.POST.get('vehiculo')
        matricula = request.POST.get('matricula')
        parking=request.POST.get('parking')
        parking = Parking.objects.get(pk=parking)
        id = parking.id

        if nombre == '' or correo == '' or telefono == '' or motivo =='' or vehiculo == '' or matricula == '' or parking=='':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('visita_visita_add')
        visita_save = Visita(
            nombre = nombre,
            correo = correo,
            telefono = telefono,
            motivo= motivo,
            vehiculo = vehiculo,
            matricula = matricula,
            parking = parking,
            )
        visita_save.save()
        messages.add_message(request, messages.INFO, 'Visita ingresada con éxito')
        Parking.objects.filter(pk=id).update(disponibilidad="Ocupado")
        return redirect('estacionamiento_estacionamiento_list')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

@login_required
def visita_visita_update(request,estacionamiento_id,parking_id):
    profile = Profile.objects.get(user_id=request.user.id)
    parking_data = Parking.objects.get(pk=parking_id)
    visita_data=Visita.objects.get(parking_id=parking_id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    estacionamiento = Estacionamiento.objects.get(pk=estacionamiento_id)
    template_name = 'visita/visita_update.html'
    return render(request,template_name,{'profile':profile,'parking_data':parking_data,'visita_data':visita_data,'estacionamiento':estacionamiento})

@login_required
def visita_visita_update_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')     
        telefono = request.POST.get('telefono')
        motivo = request.POST.get('motivo')
        vehiculo = request.POST.get('vehiculo')
        matricula = request.POST.get('matricula')
        parking=request.POST.get('parking')
        visita_data=Visita.objects.get(parking_id=parking)
        if nombre == '' or correo == '' or telefono == '' or motivo =='' or vehiculo == '' or matricula == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('visita_visita_add')
        Visita.objects.filter(pk=visita_data.id).update(nombre=nombre)
        Visita.objects.filter(pk=visita_data.id).update(correo=correo)
        Visita.objects.filter(pk=visita_data.id).update(telefono=telefono) 
        Visita.objects.filter(pk=visita_data.id).update(vehiculo=vehiculo)
        Visita.objects.filter(pk=visita_data.id).update(matricula=matricula)
        Visita.objects.filter(pk=visita_data.id).update(motivo=motivo)
        messages.add_message(request, messages.INFO, 'Visita ingresada con éxito')
        return redirect('estacionamiento_estacionamiento_list')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

@login_required
def visita_visita_delete(request,parking_id):
    profile=Profile.objects.get(user_id=request.user.id)
    if profile.group_id!= 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    visita_data=Visita.objects.get(parking_id=parking_id)
    Visita.objects.filter(pk=visita_data.id).delete()
    Parking.objects.filter(pk=parking_id).update(disponibilidad='Desocupado')
    
    messages.add_message(request, messages.INFO, 'Visita eliminada con éxito')
    return redirect('estacionamiento_estacionamiento_list')

@login_required
def visita_visita_list(request,page=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('login')
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
        h_count = Visita.objects.count()
        h_list_array = Visita.objects.all()
        for h in h_list_array:
            print(h.parking.id)
            parking=Parking.objects.get(pk=str(h.parking.id))
            estacionamiento=Estacionamiento.objects.get(nombre=parking.estacionamiento)
            piso=Piso.objects.get(num_piso=str(estacionamiento.piso))
            sucursal=piso.sucursal
            print(h_count)
            h_list.append({'id':h.id,'nombre':h.nombre,'correo':h.correo,'telefono':h.telefono,'vehiculo':h.vehiculo,
            'matricula':h.matricula,'parking':h.parking.lugar,'sucursal':sucursal,'estacionamiento':estacionamiento,'piso':piso,'count':h_count})
    else:
        h_count = Visita.objects.filter(nombre__icontains=search).count()
        
        h_list_array = Visita.objects.filter(nombre__icontains=search).order_by('nombre')
        for h in h_list_array:
            parking=Parking.objects.get(pk=str(h.parking))
            estacionamiento=Estacionamiento.objects.get(nombre=parking.estacionamiento)
            print(estacionamiento)
            piso=Piso.objects.get(num_piso=str(estacionamiento.piso))
            sucursal=piso.sucursal
            print(h_count)
            h_list.append({'id':h.id,'nombre':h.nombre,'correo':h.correo,'telefono':h.telefono,'vehiculo':h.vehiculo,'matricula':h.matricula,'parking':h.parking.lugar,'sucursal':sucursal,'estacionamiento':estacionamiento,'piso':piso,'count':h_count})            
    paginator = Paginator(h_list, 15) 
    h_list_paginate= paginator.get_page(page)   
    template_name = 'visita/visita_list.html'
    return render(request,template_name,{'template_name':template_name,'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page,'h_count':h_count,'template_name':'visita/visita_main.html'})

@login_required
def visita_visita_delete_list(request,id):
    profile=Profile.objects.get(user_id=request.user.id)
    if profile.group_id!= 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    Visita.objects.filter(pk=id).delete()
    return redirect('visita_visita_list')

@login_required
def visita_visita_update_list(request,id):
    profile = Profile.objects.get(user_id=request.user.id)
    visita_data=Visita.objects.get(pk=id)
    template_name = 'visita/visita_update_list.html'
    return render(request,template_name,{'profile':profile,'visita_data':visita_data,'template_name':'visita/visita_main.html'})

@login_required
def visita_visita_update_save_list(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')     
        telefono = request.POST.get('telefono')
        motivo = request.POST.get('motivo')
        vehiculo = request.POST.get('vehiculo')
        matricula = request.POST.get('matricula')
        parking=request.POST.get('parking')
        visita_data=Visita.objects.get(parking_id=parking)
        if nombre == '' or correo == '' or telefono == '' or motivo =='' or vehiculo == '' or matricula == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('visita_visita_add')
        Visita.objects.filter(pk=visita_data.id).update(nombre=nombre)
        Visita.objects.filter(pk=visita_data.id).update(correo=correo)
        Visita.objects.filter(pk=visita_data.id).update(telefono=telefono) 
        Visita.objects.filter(pk=visita_data.id).update(vehiculo=vehiculo)
        Visita.objects.filter(pk=visita_data.id).update(matricula=matricula)
        Visita.objects.filter(pk=visita_data.id).update(motivo=motivo)
        messages.add_message(request, messages.INFO, 'Visita ingresada con éxito')
        return redirect('visita_visita_list')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')
    
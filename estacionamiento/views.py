#nuevas importaciones 30-05-2022
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from registration.models import Profile

#fin nuevas importaciones 30-05-2022
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Avg, Q
from piso.models import Piso
from estacionamiento.models import Estacionamiento, Parking
from sucursales.models import Sucursal
from visita.models import Visita

# Create your views here.

#------------------------------------------------------------ENDPOINTS-------------------------------------------------------------------------
#Añadir multiples registros
@api_view(['POST'])
def estacionamiento_estacionamiento_add_rest(request, format=None):
    if request.method == 'POST':
        try:
            pisos=request.data['piso']
            piso=Piso.objects.get(num_piso=pisos)
            vip = request.data['vip']
            colaborador = request.data['colaborador']
            discapacitado = request.data['discapacitado']
            visita = request.data['visita']
            nombre = request.data['nombre']
            tipo_piso = piso.tipo

            if tipo_piso != "Estacionamiento":
                return Response({'Msj':"El piso ingresado no es del tipo de Estacionamiento"})

            if isinstance(vip, float):
                return Response({'Msj':"El valor ingresado en la cantidad vip no puede ser un numero decimal"})
            if isinstance(vip, str):
                return Response({'Msj':"El valor ingresado en la cantidad vip no puede ser un string o cadena de strings"})

            if isinstance(colaborador, float):
                return Response({'Msj':"El valor ingresado en la cantidad colaborador no puede ser un numero decimal"})
            if isinstance(colaborador, str):
                return Response({'Msj':"El valor ingresado en la cantidad colaborador no puede ser un string o cadena de strings"})

            if isinstance(discapacitado, float):
                return Response({'Msj':"El valor ingresado en la cantidad discapacitado no puede ser un numero decimal"})
            if isinstance(discapacitado, str):
                return Response({'Msj':"El valor ingresado en la cantidad discapacitado no puede ser un string o cadena de strings"})

            if isinstance(visita, float):
                return Response({'Msj':"El valor ingresado en la cantidad visita no puede ser un numero decimal"})
            if isinstance(visita, str):
                return Response({'Msj':"El valor ingresado en la cantidad visita no puede ser un string o cadena de strings"})

            capacidad = vip+colaborador+discapacitado+visita

            nombre_count = Estacionamiento.objects.filter(nombre=nombre).count()
            piso_count = Estacionamiento.objects.filter(piso = piso).count()

            if nombre_count>=1:
                return Response({'Msj':"Estacionamiento ya creado con ese nombre en este o otro piso"})
            if piso_count >=1:
                return Response({'Msj':"Estacionamiento ya creado en este piso"})

            estacionamiento_save = Estacionamiento(piso= piso,
            nombre=nombre,vip = vip,colaborador=colaborador,
            discapacitado=discapacitado,visita=visita,
            capacidad=capacidad)
            estacionamiento_save.save()

            estacionamiento = Estacionamiento.objects.get(nombre=nombre)
    
            valor = Parking.objects.filter(estacionamiento=estacionamiento).order_by('-lugar').first()
            if valor is None:
                numero = 1
            else:
                numero = valor.lugar
                
            inicio = 1
            while inicio <= vip:
                parking_save = Parking(estacionamiento=estacionamiento,lugar=numero,tipo="VIP")
                parking_save.save()
                inicio = inicio + 1
                numero = numero + 1

            inicio = 1
            while inicio <= colaborador:
                parking_save = Parking(estacionamiento=estacionamiento,lugar=numero,tipo="Colaborador")
                parking_save.save()
                inicio = inicio + 1
                numero = numero + 1

            inicio = 1
            while inicio <= discapacitado:
                parking_save = Parking(estacionamiento=estacionamiento,lugar=numero,tipo="Discapacitado")
                parking_save.save()
                inicio = inicio + 1
                numero = numero + 1
            
            inicio = 1
            while inicio <= visita:
                parking_save = Parking(estacionamiento=estacionamiento,lugar=numero,tipo="Visita")
                parking_save.save()
                inicio = inicio + 1
                numero = numero + 1

            return Response({'Msj':"Estacionamientos creados"})
        except Piso.DoesNotExist:
            return Response({'Msj':"Error no hay ningun piso con ese valor"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})

#Listar Registros
@api_view(['GET'])
def estacionamiento_parking_list_rest(request, format=None):
    if request.method == 'GET':
        estacionamiento_list = Parking.objects.all().order_by('id')
        estacionamiento_json = []
        for es in estacionamiento_list:
            estacionamiento_json.append({'id':es.id,'lugar':es.lugar,
            'tipo':es.tipo,'estado':es.status,'disponibilidad':es.disponibilidad})
        return Response({'List':estacionamiento_json})
    else:
        return Response({'Msj':"Error método no soportado"})

@api_view(['POST'])
def estacionamiento_estacionamiento_delete_element_rest(request, format=None):
    if request.method == 'POST':
        try:
            estacionamiento_id = request.data['estacionamiento_id']
            estacionamiento_array = Estacionamiento.objects.get(pk=estacionamiento_id)
            if estacionamiento_array:
                Estacionamiento.objects.filter(pk=estacionamiento_id).delete()
            return Response({'Msj':'Estacionamiento eliminado con exito'})
        except Estacionamiento.DoesNotExist:
            return Response({'Msj':"Error no hay ningun estacionamiento con ese valor"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})

#Añadir un registro
@api_view(['POST'])
def estacionamiento_parking_add_rest(request, format=None):
    if request.method == 'POST':
        try:
            estacionamiento = request.data['estacionamiento_id']
            tipo = request.data['tipo']
            estacionamiento = Estacionamiento.objects.get(pk=estacionamiento)
            estacionamiento_id = estacionamiento.id
            capacidad = estacionamiento.capacidad + 1
          
            valor = Parking.objects.filter(estacionamiento=estacionamiento).order_by('-lugar').first()
            if valor is None:
                numero = 1
            else:
                numero = valor.lugar + 1 
            
            if tipo == 'VIP' or tipo == 'Colaborador' or tipo == 'Discapacitado' or tipo == 'Visita': 
                estacionamiento_save = Parking(lugar=numero,tipo=tipo,estacionamiento=estacionamiento)
                estacionamiento_save.save()

                if tipo == "VIP":
                    vip = estacionamiento.vip +1
                    Estacionamiento.objects.filter(pk=estacionamiento_id).update(vip=vip)
                if tipo == "Colaborador":
                    colaborador = estacionamiento.colaborador +1
                    Estacionamiento.objects.filter(pk=estacionamiento_id).update(colaborador=colaborador)
                if tipo == "Discapacitado":
                    discapacitado = estacionamiento.discapacitado +1
                    Estacionamiento.objects.filter(pk=estacionamiento_id).update(discapacitado=discapacitado)
                if tipo == "Visita":
                    visita = estacionamiento.visita +1
                    Estacionamiento.objects.filter(pk=estacionamiento_id).update(visita=visita)

                Estacionamiento.objects.filter(pk=estacionamiento_id).update(capacidad=capacidad)

                return Response({'Msj': "Estacionamiento Creado"})
            else:
                return Response({'Msj':"No se encuentra entre los tipos de estacionamientos disponibles (VIP/Colaborador/Discapacitado/Visita)"})
        except Parking.DoesNotExist:
            return Response({'Msj':"Error no hay ningun piso con ese valor"})
        except Estacionamiento.DoesNotExist:
            return Response({'Msj':"Error no hay ningun Estacionamiento con ese valor"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
       return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def estacionamiento_parking_update_element_rest(request, format=None):
    if request.method == 'POST':
        try:
            parking_id= request.data['parking_id']
            tipo = request.data['tipo']
            if tipo == 'VIP' or tipo == 'Colaborador' or tipo == 'Discapacitado' or tipo == 'Visita':
                if tipo == '': 
                    return Response({'Msj':'Error los datos no pueden estar en blanco'})
                else:
                    if tipo !="":
                        Parking.objects.filter(pk=parking_id).update(tipo=tipo)
                    lugar_json=[]
                    lugar_array = Parking.objects.get(pk=parking_id)
                    lugar_json.append({'id':lugar_array.id,'lugar':lugar_array.lugar,'tipo':lugar_array.tipo})
                    return Response({'Msj':'Datos editados',lugar_array.lugar:lugar_json})
            else:
                return Response({'Msj':"No se encuentra entre los tipos de estacionamientos disponibles (VIP/Colaborador/Discapacitado/Visita)"})
        except Parking.DoesNotExist:
            return Response({'Msj':"Error no hay ningun lugar con ese valor"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})

#Ver un Registro
@api_view(['POST'])
def estacionamiento_parking_get_element_rest(request, format=None):
    if request.method == 'POST':
        try:
            parking_id= request.data['parking_id']
            lugar_json=[]
            lugar_array = Parking.objects.get(pk=parking_id)
            lugar_json.append(
                {'lugar':lugar_array.lugar,
                'tipo': lugar_array.tipo,
                'Estado':lugar_array.status,
                'Disponibilidad':lugar_array.disponibilidad})
            return Response({"ID: " + str(lugar_array.lugar):lugar_json})
        except Parking.DoesNotExist:
            return Response({'Msj':"Error no hay ningun lugar con ese valor"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def estacionamiento_parking_release_rest(request,format=None):
    if request.method == 'POST':
        try:
            estacionamiento_id=request.data['estacionamiento_id']
            estacionamiento = Estacionamiento.objects.get(pk=estacionamiento_id)

            lugar_count = Parking.objects.filter(estacionamiento=estacionamiento).count()

            if lugar_count > 0:
                inicio = 1
                while inicio <= lugar_count:
                    id = Parking.objects.filter(estacionamiento=estacionamiento).get(lugar=inicio)
                    if id is None:
                        pass
                    else:
                        Parking.objects.filter(estacionamiento=estacionamiento).update(disponibilidad="Desocupado")
                        Visita.objects.filter(parking_id=id).delete()  
                    
                    inicio = inicio + 1
                    
                return Response({'Msj':'Liberados'})
            else:
                return Response({'Msj':'No hay estacionamientos que liberar'})
        
        except Estacionamiento.DoesNotExist:
            return Response({'Msj':"Error no hay ningun estacionamiento en ese piso"})
        except Parking.DoesNotExist:
            return Response({'Msj':"Error no hay ningun lugar con ese valor"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def estacionamiento_parking_delete_element_rest(request, format=None):
    if request.method == 'POST':
        try:
            parking_id = request.data['parking_id']
            lugar_array = Parking.objects.get(pk=parking_id)
            estacionamiento =lugar_array.estacionamiento
            tipo = lugar_array.tipo
            estacionamiento_id = Estacionamiento.objects.get(nombre=estacionamiento)
            capacidad = estacionamiento_id.capacidad - 1

            if lugar_array:
                Parking.objects.filter(pk=parking_id).delete()
                Estacionamiento.objects.filter(nombre=estacionamiento_id).update(capacidad=capacidad)

                if tipo == "VIP":
                    vip = estacionamiento.vip - 1
                    Estacionamiento.objects.filter(nombre=estacionamiento_id).update(vip=vip)
                if tipo == "Colaborador":
                    colaborador = estacionamiento.colaborador - 1
                    Estacionamiento.objects.filter(nombre=estacionamiento_id).update(colaborador=colaborador)
                if tipo == "Discapacitado":
                    discapacitado = estacionamiento.discapacitado - 1
                    Estacionamiento.objects.filter(nombre=estacionamiento_id).update(discapacitado=discapacitado)
                if tipo == "Visita":
                    visita = estacionamiento.visita - 1
                    Estacionamiento.objects.filter(nombre=estacionamiento_id).update(visita=visita)

                Estacionamiento.objects.filter(nombre=estacionamiento_id).update(capacidad=capacidad)

                return Response({'Msj':'Lugar eliminado con exito'})
        except Parking.DoesNotExist:
            return Response({'Msj':"Error no hay ningun lugar con ese valor"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})

#filtrar por piso
#necesita validar que existe el piso
@api_view(['POST'])
def estacionamiento_parking_pisos_list_contains_rest(request, format=None):
    if request.method == 'POST':
        try:
            piso = request.data['piso']
            estacionamiento_piso = Estacionamiento.objects.get(piso=piso)
            parking_count = Parking.objects.filter(estacionamiento=estacionamiento_piso).count()
            
            if isinstance(piso, float): 
                return Response({'Msj':"El valor ingresado no puede ser un numero decimal"})
            if piso!="":
                if parking_count>0:
                    parking_list=Parking.objects.filter(estacionamiento=estacionamiento_piso)
                    parking_json=[]
                    for h in parking_list:
                        parking_json.append({'lugar':h.lugar,'tipo':h.tipo,'Estado':h.status,'Creado':h.created})
                    return Response({'piso '+str(piso):parking_json})
                else:
                    return Response({'Msj':'No tienes lugares creados'})
            else:
                return Response({'Msj':'Valor no valido'})
        except Estacionamiento.DoesNotExist:
            return Response({'Msj':"Error no hay coincidencias"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj':'Metodo no soportado'})

@api_view(['POST'])
def estacionamiento_parking_tipo_list_contains_rest(request, format=None):
    if request.method == 'POST':
        try:
            estacionamiento_id=request.data['estacionamiento_id']
            estacionamiento = Estacionamiento.objects.get(pk=estacionamiento_id)
            tipo = request.data['tipo']
            if  tipo== 'VIP' or tipo == 'Colaborador' or tipo == 'Discapacitado' or tipo == 'Visita':
                tipos_count = Parking.objects.filter(estacionamiento=estacionamiento).filter(tipo=tipo).count()
                if  tipos_count > 0:
                    tipos_list = Parking.objects.filter(estacionamiento=estacionamiento).filter(tipo=tipo)
                    tipos_json= []
                    for i in tipos_list:
                        tipos_json.append({'lugar':i.lugar,'Estado':i.status,'Creado':i.created})
                    return Response({'Listado de ' + tipo :tipos_json})
                else:
                    return Response({'Msj':"No existen tipos que concuerden en estado o nombre con la cadena"})
            else: 
                return Response({'Msj':"Tipo no valido(VIP|Colaborador|Discapacitado|Visita)"})
        except Estacionamiento.DoesNotExist:
            return Response({'Msj':"Error no hay coincidencias"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})

@api_view(['POST'])
def estacionamiento_parking_search_rest(request, format=None):
    if request.method == 'POST':
        try:
            search = request.data['search']
            if search != "":
                skill_list_count = Parking.objects.filter(Q(lugar__icontains=search)).count()
                if  skill_list_count > 0:
                    skill_list = Parking.objects.filter(Q(lugar__icontains=search))
                    skill_json= []
                    for s in skill_list:
                        skill_json.append({'lugar':s.lugar,'Tipo':s.tipo,'Estado':s.status})
                    return Response({'Listado':skill_json})
                else:
                    return Response({'Msj':"No existen lugares que contengan estos datos con la cadena"})
            else:
                return Response({'Msj':"No ha ingresado ningún valor para buscar"})
        except Parking.DoesNotExist:
            return Response({'Msj':"Error no hay coincidencias"})
        except ValueError:
            return Response({'Msj':"Valor no soportado"})
    else:
        return Response({'Msj': "Error método no soportado"})

#------------------------------------------------------------Templates-------------------------------------------------------------------------
@login_required
def estacionamiento_estacionamiento_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'estacionamiento/estacionamiento_main.html'
    return render(request,template_name,{'profile':profile,'template_name':'estacionamiento/estacionamiento_main.html'})

@login_required
def estacionamiento_estacionamiento_add(request,format=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'estacionamiento/estacionamiento_add.html'
    return render(request,template_name,{'profile':profile,'template_name':'estacionamiento/estacionamiento_main.html'})

@login_required
def estacionamiento_estacionamiento_save(request,format=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        try:
            pisos = request.POST.get('piso')
            piso=Piso.objects.get(num_piso=pisos)
            nombre = request.POST.get('nombre')
            vip = request.POST.get('vip')
            colaborador = request.POST.get('colaborador')
            discapacitado = request.POST.get('discapacitado')
            visita = request.POST.get('visita')

            vip = int(vip)
            colaborador = int(colaborador)
            discapacitado = int(discapacitado)
            visita = int(visita)
            capacidad = vip+colaborador+discapacitado+visita

            if vip < 0 or colaborador < 0 or discapacitado < 0 or visita <0 :
                messages.add_message(request, messages.INFO, 'La cantidad ingresada en VIP/Colaborador/Discapacitado/Visita no puede ser menor que 0')
                return redirect('estacionamiento_estacionamiento_add')
            if capacidad <= 0:
                messages.add_message(request, messages.INFO, 'La capacidad no puede ser menor o igual a 0')
                return redirect('estacionamiento_estacionamiento_add')
            tipo_piso = piso.tipo

            if tipo_piso != "Estacionamiento":
                messages.add_message(request, messages.INFO, 'El piso ingresado no es del tipo de Estacionamiento')
                return redirect('estacionamiento_estacionamiento_add')
            

            nombre_count = Estacionamiento.objects.filter(nombre=nombre).count()
            piso_count = Estacionamiento.objects.filter(piso = piso).count()

            if nombre_count>=1:
                messages.add_message(request, messages.INFO, 'Estacionamiento ya creado con ese nombre en este o otro piso')
                return redirect('estacionamiento_estacionamiento_add')
            if piso_count >=1:
                messages.add_message(request, messages.INFO, 'Estacionamiento ya creado en este piso')
                return redirect('estacionamiento_estacionamiento_add')
            estacionamiento_save = Estacionamiento(piso= piso,
            nombre=nombre,vip = vip,colaborador=colaborador,
            discapacitado=discapacitado,visita=visita,
            capacidad=capacidad)
            estacionamiento_save.save()

            estacionamiento = Estacionamiento.objects.get(nombre=nombre)

            valor = Parking.objects.filter(estacionamiento=estacionamiento).order_by('-lugar').first()
            if valor is None:
                numero = 1
            else:
                numero = valor.lugar
                
            inicio = 1
            while inicio <= vip:
                parking_save = Parking(estacionamiento=estacionamiento,lugar=numero,tipo="VIP")
                parking_save.save()
                inicio = inicio + 1
                numero = numero + 1

            inicio = 1
            while inicio <= colaborador:
                parking_save = Parking(estacionamiento=estacionamiento,lugar=numero,tipo="Colaborador")
                parking_save.save()
                inicio = inicio + 1
                numero = numero + 1

            inicio = 1
            while inicio <= discapacitado:
                parking_save = Parking(estacionamiento=estacionamiento,lugar=numero,tipo="Discapacitado")
                parking_save.save()
                inicio = inicio + 1
                numero = numero + 1
            
            inicio = 1
            while inicio <= visita:
                parking_save = Parking(estacionamiento=estacionamiento,lugar=numero,tipo="Visita")
                parking_save.save()
                inicio = inicio + 1
                numero = numero + 1

            messages.add_message(request, messages.INFO, 'Estacionamientos creados')
            return redirect('estacionamiento_estacionamiento_list')
        except Piso.DoesNotExist:
            messages.add_message(request, messages.INFO, 'No hay ningun piso con ese valor')
            return redirect('estacionamiento_estacionamiento_add')
        except ValueError:
            messages.add_message(request, messages.INFO, 'El valor ingresado en el piso no es soportado')
            return redirect('estacionamiento_estacionamiento_add')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

@login_required
def estacionamiento_estacionamiento_list(request,page=None,search=None):
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
    p_list = []
    if search == None or search == "None":
        p_count = Estacionamiento.objects.filter(status='Activo').count()
        p_list_array = Estacionamiento.objects.filter(status='Activo').order_by('piso')
        for p in p_list_array:
            piso_id = Piso.objects.get(num_piso = p.piso.num_piso)
            sucursal_id = piso_id.sucursal
            p_list.append({'id':p.id,'piso':p.piso,'sucursal':sucursal_id,'nombre':p.nombre,'vip':p.vip,'colaborador':p.colaborador,'visita':p.visita,'discapacitado':p.discapacitado,'capacidad':p.capacidad})
    else:
        p_count = Estacionamiento.objects.filter(status='Activo').filter(Q(nombre__icontains=search)).count()
        p_list_array = Estacionamiento.objects.filter(status='Activo').filter(Q(nombre__icontains=search)).order_by('piso')
        for p in p_list_array:
            piso_id = Piso.objects.get(num_piso = p.piso.num_piso)
            sucursal_id = piso_id.sucursal
            p_list.append({'id':p.id,'piso':p.piso,'sucursal':sucursal_id,'nombre':p.nombre,'vip':p.vip,'colaborador':p.colaborador,'visita':p.visita,'discapacitado':p.discapacitado,'capacidad':p.capacidad})      
    paginator = Paginator(p_list, 5)
    p_list_paginate= paginator.get_page(page)
    template_name = 'estacionamiento/estacionamiento_list.html'
    return render(request,template_name,{'template_name':template_name,'p_list_paginate':p_list_paginate,'paginator':paginator,'page':page,'search':search,'template_name':'estacionamiento/estacionamiento_main.html'})

@login_required
def estacionamiento_estacionamiento_delete(request,estacionamiento_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        estacionamiento_array = Estacionamiento.objects.get(pk=estacionamiento_id)
        if estacionamiento_array:
            Estacionamiento.objects.filter(pk=estacionamiento_id).delete()
            messages.add_message(request, messages.INFO, 'Estacionamiento eliminado con exito')
            return redirect('estacionamiento_estacionamiento_list')
    except Estacionamiento.DoesNotExist:
        messages.add_message(request, messages.INFO, 'No hay ningun estacionamiento con ese valor')
        return redirect('estacionamiento_estacionamiento_list')
    except ValueError:
        messages.add_message(request, messages.INFO, 'Valor no soportado')
        return redirect('estacionamiento_estacionamiento_list')

@login_required
def estacionamiento_parking_list_piso(request,estacionamiento_id,page=None,search=None):
    try:
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
    
        p_list = []
        if search == None or search=='' or search == "None":
            parking_count = Parking.objects.filter(estacionamiento=estacionamiento_id).count()
            p_list_array = Parking.objects.filter(status='Activo').filter(estacionamiento=estacionamiento_id).order_by('lugar')
            for p in p_list_array:
                estacionamiento = Estacionamiento.objects.get(pk=p.estacionamiento_id)
                p_list.append({'id':p.id,'lugar':p.lugar,'tipo':p.tipo,'status':p.status,'disponibilidad':p.disponibilidad,'piso':estacionamiento.piso})
        else:
            parking_count = Parking.objects.filter(estacionamiento=estacionamiento_id).count()
            p_list_array = Parking.objects.filter(status='Activo').filter(estacionamiento=estacionamiento_id).filter(lugar=search).order_by('lugar')
            for p in p_list_array:
                estacionamiento = Estacionamiento.objects.get(pk=p.estacionamiento_id)
                p_list.append({'id':p.id,'lugar':p.lugar,'tipo':p.tipo,'status':p.status,'disponibilidad':p.disponibilidad,'piso':estacionamiento.piso})

        estacionamiento = Estacionamiento.objects.get(pk=estacionamiento_id)
        piso_n = estacionamiento.piso
        sucursal = piso_n.sucursal

        VIP="VIP"
        Colaborador="Colaborador"
        Discapacitado="Discapacitado"
        Visita="Visita"
        paginator = Paginator(p_list, 20) 
        p_list_paginate= paginator.get_page(page) 
        template_name = 'parking/parking_list.html'

        return render(request,template_name,{'template_name':template_name,'p_list_paginate':p_list_paginate,'paginator':paginator,'page':page,
        'sucursal':sucursal,'estacionamiento':estacionamiento,'search':search,
        'VIP':VIP,'Colaborador':Colaborador,'Discapacitado':Discapacitado,'Visita':Visita,'p_list':p_list,'template_name':'estacionamiento/estacionamiento_main.html'})
    except Parking.DoesNotExist:
        messages.add_message(request, messages.INFO, 'No existe ningun parking con ese valor')
        return redirect('estacionamiento_estacionamiento_list')
    except ValueError:
        messages.add_message(request, messages.INFO, 'Valor no soportado')
        return redirect('estacionamiento_estacionamiento_list')

@login_required
def estacionamiento_parking_list_tipo(request,estacionamiento_id,tipo,format=None,page=None,search=None):
    try:
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
        p_list = []
        if search == None or search=='' or search == "None":
            p_list_array = Parking.objects.filter(status='Activo').filter(estacionamiento=estacionamiento_id).filter(tipo=tipo).order_by('lugar')
            for p in p_list_array:
                estacionamiento = Estacionamiento.objects.get(pk=p.estacionamiento_id)
                p_list.append({'id':p.id,'lugar':p.lugar,'tipo':p.tipo,'status':p.status,'disponibilidad':p.disponibilidad,'piso':estacionamiento.piso})
        else:
            p_list_array = Parking.objects.filter(status='Activo').filter(estacionamiento=estacionamiento_id).filter(tipo=tipo).filter(lugar=search).order_by('lugar')
            for p in p_list_array:
                estacionamiento = Estacionamiento.objects.get(pk=p.estacionamiento_id)
                p_list.append({'id':p.id,'lugar':p.lugar,'tipo':p.tipo,'status':p.status,'disponibilidad':p.disponibilidad,'piso':estacionamiento.piso})
            
        estacionamiento= Estacionamiento.objects.get(pk=estacionamiento_id)
        piso_n = estacionamiento.piso
        sucursal = piso_n.sucursal

        VIP="VIP"
        Colaborador="Colaborador"
        Discapacitado="Discapacitado"
        Visita="Visita"
        paginator = Paginator(p_list, 20) 
        p_list_paginate= paginator.get_page(page)

        template_name = 'parking/parking_list.html'
        return render(request,template_name,{'template_name':template_name,'p_list_paginate':p_list_paginate,'paginator':paginator,'page':page,
        'sucursal':sucursal,'estacionamiento':estacionamiento,
        'VIP':VIP,'Colaborador':Colaborador,'Discapacitado':Discapacitado,'Visita':Visita,'p_list':p_list,'template_name':'estacionamiento/estacionamiento_main.html'})
    except Parking.DoesNotExist:
        messages.add_message(request, messages.INFO, 'No existe ningun parking con ese valor')
        return redirect('estacionamiento_estacionamiento_list')
    except ValueError:
        messages.add_message(request, messages.INFO, 'Valor no soportado')
        return redirect('estacionamiento_estacionamiento_list')

@login_required
def estacionamiento_parking_add(request,estacionamiento_id,format=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    estacionamiento = Estacionamiento.objects.get(pk=estacionamiento_id)
    template_name = 'parking/parking_add.html'
    return render(request,template_name,{'profile':profile,'estacionamiento':estacionamiento,'template_name':'estacionamiento/estacionamiento_main.html'})

@login_required
def estacionamiento_parking_save(request,estacionamiento_id,format=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        try:
            estacionamiento = Estacionamiento.objects.get(pk=estacionamiento_id)
            tipo = request.POST.get('tipo')
            estacionamiento_id = estacionamiento.id
            capacidad = estacionamiento.capacidad + 1
        
            valor = Parking.objects.filter(estacionamiento=estacionamiento).order_by('-lugar').first()
            if valor is None:
                numero = 1
            else:
                numero = valor.lugar + 1 
            
            if tipo == 'VIP' or tipo == 'Colaborador' or tipo == 'Discapacitado' or tipo == 'Visita': 
                estacionamiento_save = Parking(lugar=numero,tipo=tipo,estacionamiento=estacionamiento)
                estacionamiento_save.save()

                if tipo == "VIP":
                    vip = estacionamiento.vip +1
                    Estacionamiento.objects.filter(pk=estacionamiento_id).update(vip=vip)
                if tipo == "Colaborador":
                    colaborador = estacionamiento.colaborador +1
                    Estacionamiento.objects.filter(pk=estacionamiento_id).update(colaborador=colaborador)
                if tipo == "Discapacitado":
                    discapacitado = estacionamiento.discapacitado +1
                    Estacionamiento.objects.filter(pk=estacionamiento_id).update(discapacitado=discapacitado)
                if tipo == "Visita":
                    visita = estacionamiento.visita +1
                    Estacionamiento.objects.filter(pk=estacionamiento_id).update(visita=visita)

                Estacionamiento.objects.filter(pk=estacionamiento_id).update(capacidad=capacidad)
                messages.add_message(request, messages.INFO, 'Lugar de estacionamiento creado')
                return redirect('estacionamiento_parking_list_piso',estacionamiento.id)
            else:
                messages.add_message(request, messages.INFO, 'No se encuentra entre los tipos de estacionamientos disponibles (VIP/Colaborador/Discapacitado/Visita)')
                return redirect('estacionamiento_parking_add',estacionamiento.id)
        except Estacionamiento.DoesNotExist:
            messages.add_message(request, messages.INFO, 'No hay ningun estacionamiento con ese valor')
            return redirect('estacionamiento_parking_add',estacionamiento.id)
        except ValueError:
            messages.add_message(request, messages.INFO, 'Valor no soportado')
            return redirect('estacionamiento_parking_add',estacionamiento.id)
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

@login_required
def estacionamiento_parking_ver(request,parking_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try :
        parking_data = Parking.objects.get(pk=parking_id)
        estacionamiento = parking_data.estacionamiento
        estacionamiento = Estacionamiento.objects.get(nombre=estacionamiento)
        template_name = 'parking/parking_ver.html'
        return render(request,template_name,{'profile':profile,'parking_data':parking_data,'estacionamiento':estacionamiento,'template_name':'estacionamiento/estacionamiento_main.html'})
    except Parking.DoesNotExist:
        messages.add_message(request, messages.INFO, 'No existe ningun parking con ese valor')
        return redirect('estacionamiento_estacionamiento_list')
    except ValueError:
        messages.add_message(request, messages.INFO, 'Valor no soportado')
        return redirect('estacionamiento_estacionamiento_list')

@login_required
def estacionamiento_parking_update(request,parking_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        try:
            parking = Parking.objects.get(pk=parking_id)
            
            estacionamiento = parking.estacionamiento
            estacionamiento = Estacionamiento.objects.get(nombre=estacionamiento)
            estacionamiento_id=estacionamiento.id
            tipo_anterior = parking.tipo
            tipo = request.POST.get('tipo')
            parking = parking.id

            if tipo == 'VIP' or tipo == 'Colaborador' or tipo == 'Discapacitado' or tipo == 'Visita':
                if tipo == '':
                    messages.add_message(request, messages.INFO, 'Error los datos no pueden estar en blanco')
                    return redirect('estacionamiento_parking_ver',parking_id)
                else:
                    if tipo_anterior == "VIP":
                        vip_anterior = estacionamiento.vip - 1
                        Estacionamiento.objects.filter(pk=estacionamiento_id).update(vip=vip_anterior)
                    if tipo_anterior == "Colaborador":
                        colaborador_anterior = estacionamiento.colaborador -1
                        Estacionamiento.objects.filter(pk=estacionamiento_id).update(colaborador=colaborador_anterior)
                    if tipo_anterior == "Discapacitado":
                        discapacitado_anterior = estacionamiento.discapacitado - 1
                        Estacionamiento.objects.filter(pk=estacionamiento_id).update(discapacitado=discapacitado_anterior)
                    if tipo_anterior == "Visita":
                        visita_anterior = estacionamiento.visita -1
                        Estacionamiento.objects.filter(pk=estacionamiento_id).update(visita=visita_anterior)

                    if tipo == "VIP":
                        vip = estacionamiento.vip +1
                        Estacionamiento.objects.filter(pk=estacionamiento_id).update(vip=vip)
                    if tipo == "Colaborador":
                        colaborador = estacionamiento.colaborador +1
                        Estacionamiento.objects.filter(pk=estacionamiento_id).update(colaborador=colaborador)
                    if tipo == "Discapacitado":
                        discapacitado = estacionamiento.discapacitado +1
                        Estacionamiento.objects.filter(pk=estacionamiento_id).update(discapacitado=discapacitado)
                    if tipo == "Visita":
                        visita = estacionamiento.visita +1
                        Estacionamiento.objects.filter(pk=estacionamiento_id).update(visita=visita)
                    Parking.objects.filter(pk=parking).update(tipo=tipo)

                    messages.add_message(request, messages.INFO, 'Parking editado con exito')
                    return redirect('estacionamiento_parking_list_piso',estacionamiento.id)
            else:
                messages.add_message(request, messages.INFO, 'No se encuentra entre los tipos de estacionamientos disponibles (VIP/Colaborador/Discapacitado/Visita)')
                return redirect('estacionamiento_parking_ver',parking_id)
        except Parking.DoesNotExist:
            messages.add_message(request, messages.INFO, 'No se encuentra entre los tipos de estacionamientos disponibles (VIP/Colaborador/Discapacitado/Visita)')
            return redirect('estacionamiento_parking_list_piso',estacionamiento.id)
        except ValueError:
            messages.add_message(request, messages.INFO, 'Valor no soportado')
            return redirect('estacionamiento_parking_list_piso',estacionamiento.id)
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

@login_required
def estacionamiento_parking_delete(request,parking_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    try:
        parking = Parking.objects.get(pk=parking_id)
        parking_id_n = parking.id

        estacionamiento =parking.estacionamiento
        tipo = parking.tipo
        estacionamiento_id = Estacionamiento.objects.get(nombre=estacionamiento)
        capacidad = estacionamiento_id.capacidad - 1

        if parking:
            if tipo == "VIP":
                vip = estacionamiento.vip - 1
                Estacionamiento.objects.filter(nombre=estacionamiento_id).update(vip=vip)
            if tipo == "Colaborador":
                colaborador = estacionamiento.colaborador - 1
                Estacionamiento.objects.filter(nombre=estacionamiento_id).update(colaborador=colaborador)
            if tipo == "Discapacitado":
                discapacitado = estacionamiento.discapacitado - 1
                Estacionamiento.objects.filter(nombre=estacionamiento_id).update(discapacitado=discapacitado)
            if tipo == "Visita":
                visita = estacionamiento.visita - 1
                Estacionamiento.objects.filter(nombre=estacionamiento_id).update(visita=visita)

            Parking.objects.filter(pk=parking_id_n).delete()
            Estacionamiento.objects.filter(nombre=estacionamiento_id).update(capacidad=capacidad)
            
            messages.add_message(request, messages.INFO, 'Lugar eliminado con exito')
            return redirect('estacionamiento_parking_list_piso',estacionamiento_id.id)
    except Parking.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error no hay ningun lugar con ese valor')
        return redirect('estacionamiento_estacionamiento_list')
    except ValueError:
        messages.add_message(request, messages.INFO, 'Valor no soportado')
        return redirect('estacionamiento_estacionamiento_list')

@login_required
def estacionamiento_parking_release(request,estacionamiento_id,format=None):
    try:
        #estacionamiento = Estacionamiento.objects.get(pk=estacionamiento_id)
        p_list_array = Parking.objects.filter(status='Activo').filter(estacionamiento=estacionamiento_id).order_by('lugar')
        for p in p_list_array:
            Parking.objects.filter(pk=p.id).update(disponibilidad="Desocupado")
            Visita.objects.filter(parking_id=p.id).delete()
        messages.add_message(request, messages.INFO, 'Estacionamientos liberados')
        return redirect('estacionamiento_parking_list_piso',estacionamiento_id)
    except Estacionamiento.DoesNotExist:
        messages.add_message(request, messages.INFO, 'Error no hay ningun estacionamiento en ese piso')
        return redirect('estacionamiento_parking_list_piso',estacionamiento_id)
    except Parking.DoesNotExist:
        messages.add_message(request, messages.INFO, 'No hay ningun lugar con ese valor')
        return redirect('estacionamiento_parking_list_piso',estacionamiento_id)
    except ValueError:
        messages.add_message(request, messages.INFO, 'Valor no soportado')
        return redirect('estacionamiento_parking_list_piso',estacionamiento_id)

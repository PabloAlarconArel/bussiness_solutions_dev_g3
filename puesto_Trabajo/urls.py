from django.urls import path
from sucursales import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
puesto_Trabajo_urlpatterns = [

    path('puesto_Trabajo_main/',views.puesto_Trabajo_main,name="puesto_Trabajo_main"),
    path('puesto_Trabajo_puesto_add/',views.puesto_Trabajo_puesto_add,name="puesto_Trabajo_puesto_add"),
    path('puesto_Trabajo_puesto_save/',views.puesto_Trabajo_puesto_save,name="puesto_Trabajo_puesto_save"),
    path('puesto_Trabajos_puesto_ver/<puesto_id>/',views.puesto_Trabajo_puesto_ver,name="puesto_Trabajo_puesto_ver"),
    path('puesto_Trabajo_list_puesto_Trabajo/',views.puesto_Trabajo_list_puesto_puesto,name="puesto_Trabajo_list_puesto_Trabajo"),

    #endPoints
    path('puesto_Trabajo_puesto_add_rest/', views.puesto_Trabajo_puesto_add_rest),  
    path('puesto_Trabajo_puesto_list_rest/', views.puesto_Trabajo_puesto_list_rest),
    path('puesto_Trabajo_sucursal_get_element_rest/', views.puesto_Trabajo_puesto_get_element_rest),
    path('puesto_Trabajo_sucursal_update_element_rest/', views.puesto_Trabajo_puesto_update_element_rest),
    path('puesto_Trabajo_sucursal_del_element_rest/', views.puesto_Trabajo_puesto_del_element_rest)
    ]
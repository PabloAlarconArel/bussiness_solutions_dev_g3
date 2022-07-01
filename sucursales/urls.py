
from django.urls import path
from sucursales import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
sucursales_urlpatterns = [
    path('sucursales_sucursal_delete/<sucursal_id>',views.sucursales_sucursal_delete,name="sucursales_sucursal_delete"),
    path('sucursales_sucursal_update/',views.sucursales_sucursal_update,name="sucursales_sucursal_update"),
    path('sucursales_main/',views.sucursales_main,name="sucursales_main"),
    path('sucursales_master_menu/',views.sucursales_master_menu,name="sucursales_master_menu"),
    path('sucursales_sucursal_add/',views.sucursales_sucursal_add,name="sucursales_sucursal_add"),
    path('sucursales_sucursal_save/',views.sucursales_sucursal_save,name="sucursales_sucursal_save"),
    path('sucursales_sucursal_ver/<sucursal_id>/',views.sucursales_sucursal_ver,name="sucursales_sucursal_ver"),
    path('sucursales_list_sucursales/',views.sucursales_list_sucursales,name="sucursales_list_sucursales"),

    #endPoints
    path('sucursales_sucursal_add_rest/', views.sucursales_sucursal_add_rest),  
    path('sucursales_sucursal_list_rest/', views.sucursales_sucursal_list_rest),
    path('sucursales_sucursal_get_element_rest/', views.sucursales_sucursal_get_element_rest),
    path('sucursales_sucursal_update_element_rest/', views.sucursales_sucursal_update_element_rest),
    path('sucursales_sucursal_del_element_rest/', views.sucursales_sucursal_del_element_rest)
    ]
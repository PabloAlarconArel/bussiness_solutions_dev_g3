
from django.urls import path
from sucursales import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
sucursales_urlpatterns = [
    #endPoints
    path('sucursales_sucursal_add_rest/', views.sucursales_sucursal_add_rest),  
    path('sucursales_sucursal_list_rest/', views.sucursales_sucursal_list_rest),
    path('sucursales_sucursal_get_element_rest/', views.sucursales_sucursal_get_element_rest),
    path('sucursales_sucursal_update_element_rest/', views.sucursales_sucursal_update_element_rest),
    path('sucursales_sucursal_del_element_rest/', views.sucursales_sucursal_del_element_rest)
    ]
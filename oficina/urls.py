from django.urls import path
from oficina import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
oficina_urlpatterns = [
    #endPoints
     path('oficinas_oficina_add_rest/', views.oficinas_oficina_add_rest),
     path('oficinas_oficina_list_rest/', views.oficinas_oficina_list_rest),
     path('oficinas_oficina_update_element_rest/', views.oficinas_oficina_update_element_rest),
     path('oficinas_oficina_get_element_rest/', views.oficinas_oficina_get_element_rest),
     path('oficinas_oficina_del_element_rest/', views.oficinas_oficina_del_element_rest),

    path('oficinas_main/', views.oficinas_main, name="oficinas_main"),
    path('oficinas_oficina_add/', views.oficinas_oficina_add, name="oficinas_oficina_add"),
    path('oficinas_oficina_save/', views.oficinas_oficina_save, name="oficinas_oficina_save"),
    path('oficinas_oficina_ver/<oficina_id>/', views.oficinas_oficina_ver, name="oficinas_oficina_ver"),
    path('oficinas_list_oficinas/', views.oficinas_list_oficinas, name="oficinas_list_oficinas"),
    ]
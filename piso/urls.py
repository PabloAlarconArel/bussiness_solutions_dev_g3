from django.urls import path
from piso import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

piso_urlpatterns = [
    path('pisos_piso_main/',views.pisos_piso_main,name="pisos_piso_main"),
    path('pisos_piso_add/',views.pisos_piso_add,name="pisos_piso_add"),
    path('pisos_piso_save/',views.pisos_piso_save,name="pisos_piso_save"),
    path('pisos_list_piso/',views.pisos_list_piso,name="pisos_list_piso"),
    path('pisos_piso_ver/<id>/',views.pisos_piso_ver,name="pisos_piso_ver"),
    path('pisos_piso_update/',views.pisos_piso_update,name="pisos_piso_update"),
    path('pisos_piso_delete/<id>/',views.pisos_piso_delete,name="pisos_piso_delete"),

    #endPoints
    path('pisos_piso_add_rest/', views.pisos_piso_add_rest),
    path('pisos_piso_list_rest/', views.pisos_piso_list_rest),
    path('pisos_piso_update_element_rest/', views.pisos_piso_update_element_rest),
    path('pisos_piso_get_element_rest/', views.pisos_piso_get_element_rest),
    path('pisos_piso_del_element_rest/', views.pisos_piso_del_element_rest)
    ]
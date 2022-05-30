from django.urls import path
from piso import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

piso_urlpatterns = [
    #endPoints
    path('pisos_piso_add_rest/', views.pisos_piso_add_rest),
    path('pisos_piso_list_rest/', views.pisos_piso_list_rest),
    path('pisos_piso_update_element_rest/', views.pisos_piso_update_element_rest),
    path('pisos_piso_get_element_rest/', views.pisos_piso_get_element_rest),
    path('pisos_piso_del_element_rest/', views.pisos_piso_del_element_rest)
    ]
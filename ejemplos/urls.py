from django.urls import path
from ejemplos import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
ejemplos_urlpatterns = [
    #endPoints
    path('ejemplos_habilidad_add_rest/', views.ejemplos_habilidad_add_rest),  
    path('ejemplos_habilidad_list_rest/', views.ejemplos_habilidad_list_rest),  
    ]

    
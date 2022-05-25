from django.urls import path
from sala import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
sala_urlpatterns = [
    #endPoints
    path('sala_salas_list_contains/', views.sala_salas_list_contains),
    path('sala_salas_update_element_rest/', views.sala_salas_update_element_rest)
    ]
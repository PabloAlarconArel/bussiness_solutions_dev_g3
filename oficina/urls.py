from django.urls import path
from oficina import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
oficina_urlpatterns = [
    #endPoints
     path('oficina_oficina_list_rest/', views.oficina_oficina_list_rest),
    path('oficina_oficina_update_element_rest/', views.oficina_oficina_update_element_rest)
    ]
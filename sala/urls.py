from django.urls import path
from sala import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
sala_urlpatterns = [
    #endPoints
    path('salas_sala_add_rest/', views.salas_sala_add_rest),
    path('salas_sala_list_rest/', views.salas_sala_list_rest),
    path('salas_sala_update_element_rest/', views.salas_sala_update_element_rest),
    path('salas_sala_get_element_rest/', views.salas_sala_get_element_rest),
    path('salas_sala_del_element_rest/', views.salas_sala_del_element_rest),
    
    path('salas_main/', views.salas_main, name="salas_main"),
    path('salas_sala_add/', views.salas_sala_add, name="salas_sala_add"),
    path('salas_sala_save/', views.salas_sala_save, name="salas_sala_save"),
    path('salas_sala_ver/<sala_id>/', views.salas_sala_ver, name="salas_sala_ver"),
    path('salas_list_salas/', views.salas_list_salas, name="salas_list_salas"),
    ]
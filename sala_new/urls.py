from django.urls import path
from sala_new import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
sala_new_urlpatterns = [

    path('sala_new_main/', views.sala_new_main, name="sala_new_main"),
    path('sala_new_sala_add/', views.sala_new_sala_add, name="sala_new_sala_add"),
    path('sala_new_sala_save/', views.sala_new_sala_save, name="sala_new_sala_save"),
    path('sala_new_sala_ver/<sala_id>/', views.sala_new_sala_ver, name="sala_new_sala_ver"),
    path('sala_new_list_sala_new/', views.sala_new_list_sala_new, name="sala_new_list_sala_new"),
    path('sala_new_sala_update/',views.sala_new_sala_update,name="sala_new_sala_update"),

    #endPoints
    path('salas_sala_add_rest/', views.salas_sala_add_rest),
    path('salas_sala_list_rest/', views.salas_sala_list_rest),
    path('salas_sala_update_element_rest/', views.salas_sala_update_element_rest),
    path('salas_sala_get_element_rest/', views.salas_sala_get_element_rest),
    path('salas_sala_del_element_rest/', views.salas_sala_del_element_rest),
    
    
]
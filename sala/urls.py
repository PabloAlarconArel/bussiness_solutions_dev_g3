from django.urls import path
from sala import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
sala_urlpatterns = [
    #endPoints
    path('sala_sala_add_rest/', views.sala_sala_add_rest),
    path('sala_sala_list_rest/', views.sala_sala_list_rest),
    path('sala_sala_update_element_rest/', views.sala_sala_update_element_rest),
    path('sala_sala_get_element_rest/', views.sala_sala_get_element_rest),
    path('sala_sala_del_element_rest/', views.sala_sala_del_element_rest)
    ]
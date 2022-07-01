from django.urls import path,include
from estacionamiento import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


estacionamiento_urlpatterns = [
    path('estacionamiento_main/',views.estacionamiento_estacionamiento_main,name="estacionamiento_estacionamiento_main"),
    path('estacionamiento_list/',views.estacionamiento_estacionamiento_list,name="estacionamiento_estacionamiento_list"),
    path('estacionamiento_add/',views.estacionamiento_estacionamiento_add,name="estacionamiento_estacionamiento_add"),
    path('estacionamiento_save/',views.estacionamiento_estacionamiento_save,name="estacionamiento_estacionamiento_save"),
    path('estacionamiento_delete/<estacionamiento_id>',views.estacionamiento_estacionamiento_delete,name="estacionamiento_estacionamiento_delete"),


    path('parking_list/<estacionamiento_id>/',views.estacionamiento_parking_list_piso,name="estacionamiento_parking_list_piso"),

    path('parking_list_tipo/<estacionamiento_id>/<str:tipo>/',views.estacionamiento_parking_list_tipo,name="estacionamiento_parking_list_tipo"),

    
    path('<estacionamiento_id>/parking_add/',views.estacionamiento_parking_add,name="estacionamiento_parking_add"),
    path('<estacionamiento_id>/parking_release/',views.estacionamiento_parking_release,name="estacionamiento_parking_release"),
    path('<estacionamiento_id>/parking_save/',views.estacionamiento_parking_save,name="estacionamiento_parking_save"),
    path('parking_ver/<parking_id>/',views.estacionamiento_parking_ver,name="estacionamiento_parking_ver"),
    path('parking_delete/<parking_id>/',views.estacionamiento_parking_delete,name="estacionamiento_parking_delete"),
    path('parking_update/<parking_id>/',views.estacionamiento_parking_update,name="estacionamiento_parking_update"),


    #Endpoints
    #Estacionamientos
    path('estacionamiento_estacionamiento_add_rest/',views.estacionamiento_estacionamiento_add_rest),
    path('estacionamiento_estacionamiento_delete_element_rest/',views.estacionamiento_estacionamiento_delete_element_rest),
    #Parking
    path('estacionamiento_parking_add_rest/',views.estacionamiento_parking_add_rest),
    path('estacionamiento_parking_update_element_rest/',views.estacionamiento_parking_update_element_rest),
    path('estacionamiento_parking_delete_element_rest/',views.estacionamiento_parking_delete_element_rest),
    path('estacionamiento_parking_list_rest/',views.estacionamiento_parking_list_rest),
    path('estacionamiento_parking_get_element_rest/',views.estacionamiento_parking_get_element_rest),
    path('estacionamiento_parking_search_rest/',views.estacionamiento_parking_search_rest),
    path('estacionamiento_parking_release_rest/',views.estacionamiento_parking_release_rest),
    path('estacionamiento_parking_pisos_list_contains_rest/',views.estacionamiento_parking_pisos_list_contains_rest),
    path('estacionamiento_parking_tipo_list_contains_rest/',views.estacionamiento_parking_tipo_list_contains_rest),
]
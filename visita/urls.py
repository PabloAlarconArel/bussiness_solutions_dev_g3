from django.urls import path,include
from visita import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


visita_urlpatterns = [
    path('visita_visita_add_rest/',views.visita_visita_add_rest),
    path('visita_visita_list_rest/',views.visita_visita_list_rest),
    path('visita_visita_search_rest/',views.visita_visita_search_rest),
    path('visita_visita_update_element_rest/',views.visita_visita_update_element_rest),
    path('visita_visita_delete_element_rest/',views.visita_visita_delete_element_rest),

    #TEMPLATES
    path('visita_main/',views.visita_visita_main,name="visita_visita_main"),
    path('visita_visita_list/',views.visita_visita_list,name="visita_visita_list"),
    path('visita_visita_add/<estacionamiento_id>/<parking_id>/',views.visita_visita_add,name="visita_visita_add"),
    path('visita_visita_save/',views.visita_visita_save,name="visita_visita_save"),
    path('visita_visita_update/<estacionamiento_id>/<parking_id>',views.visita_visita_update,name="visita_visita_update"),
    path('visita_visita_update_save/',views.visita_visita_update_save,name="visita_visita_update_save"),
    path('visita_visita_delete/<parking_id>',views.visita_visita_delete,name="visita_visita_delete"),

    path('visita_visita_delete_list/<id>',views.visita_visita_delete_list,name="visita_visita_delete_list"),
    path('visita_visita_update_list/<id>',views.visita_visita_update_list,name="visita_visita_update_list"),
    path('visita_visita_update_save_list/',views.visita_visita_update_save_list,name="visita_visita_update_save_list"),
    
]  
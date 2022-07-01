from unicodedata import name
from django.urls import path
from accesos import views
from rest_framework.urlpatterns import format_suffix_patterns


accesos_urlspatterns = [ 
    #endpoint guardar
    path('accesos_ingreso_add_rest/', views.accesos_ingreso_add_rest),
    path('accesos_ingreso_del_element_rest/' , views.accesos_ingreso_del_element_rest),
    path('accesos_ingreso_update_element_rest/' , views.accesos_ingreso_update_element_rest),
    path('accesos_ingreso_get_element_rest/' , views.accesos_ingreso_get_element_rest),
    path('accesos_ingreso_list_range_date_rest/', views.accesos_ingreso_list_range_date_rest),  
    path('accesos_ingreso_list_rest/', views.accesos_ingreso_list_rest),
    path('accesos_ingreso_search_rest/',views.accesos_ingreso_search_rest),
    path('accesos_ingreso_tipo_list_contains_rest/',views.accesos_ingreso_tipo_list_contains_rest),
    #path('accesos_parking_release_rest/' , views.accesos_parking_release_rest),
    
    
    ######TEMPLATES######
    path('acceso_main/' , views.accesos_accesos_main,name="acceso_acceso_main"),
    path('acceso_create_add/<parking_id>' , views.acceso_create_add,name="acceso_create_add"),
    path('acceso_create_save/' , views.acceso_create_save,name="acceso_create_save"),
    path('acceso_ingreso_update/<parking_id>' , views.acceso_ingreso_update,name="acceso_ingreso_update"),
    path('acceso_ingreso_update_save/' , views.acceso_ingreso_update_save, name="acceso_ingreso_update_save"),
    path('acceso_ingreso_delete/<parking_id>' , views.acceso_ingreso_delete,name="acceso_ingreso_delete"),
    path('acceso_ingreso_list' , views.acceso_ingreso_list, name="acceso_ingreso_list"),
    path('acceso_ingreso_ver' , views.acceso_ingreso_ver, name="acceso_ingreso_ver" )
]

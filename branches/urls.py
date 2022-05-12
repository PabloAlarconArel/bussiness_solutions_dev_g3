from django.urls import path
from branches import views #importará los métodos que generemos en nuestra app
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
branches_urlpatterns = [
    #endPoints
    path('branches_branch_add_rest/', views.branches_branch_add_rest),  
    path('branches_branch_list_rest/', views.branches_branch_list_rest),  
    ]
from django.contrib import admin
from estacionamiento.models import Parking,Estacionamiento


# Register your models here.
class ParkingAdmin(admin.ModelAdmin):
    list_display =("lugar","tipo","disponibilidad")
    readonly_fields=('created','updated')

admin.site.register(Parking,ParkingAdmin)
admin.site.register(Estacionamiento)
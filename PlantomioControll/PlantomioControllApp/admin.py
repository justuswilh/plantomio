from django.contrib import admin
from .models import Device, PlantGroup, TankGroup, ClimateGroup

admin.site.register(Device)
admin.site.register(PlantGroup)
admin.site.register(TankGroup)
admin.site.register(ClimateGroup)
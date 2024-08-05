from django.contrib import admin
from django.urls import include, path
from PlantomioControllApp import views  # Importieren Sie Ihre Views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.devices_view, name='Devices'),  
    path('plant-plan/', views.plant_plan_view, name='plant_plan_view'),
]
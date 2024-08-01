from django.contrib import admin
from django.urls import include, path
from PlantomioControllApp import views  # Importieren Sie Ihre Views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.devices_view, name='Devices'),  # Beispielroute
]
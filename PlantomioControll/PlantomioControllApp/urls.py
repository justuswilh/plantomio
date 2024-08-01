from django.urls import path
from .views import devices_view

urlpatterns = [
    path('devices/', devices_view, name='Devices'),
]
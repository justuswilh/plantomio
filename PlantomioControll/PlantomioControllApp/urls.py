from django.urls import path
from . import views

urlpatterns = [
    path('devices/', views.devices_view, name='devices_view'),
    path('plant-plan/', views.plant_plan_view, name='plant_plan_view'),
]

from django.shortcuts import render
from .models import Device, PlantGroup, TankGroup, ClimateGroup, PlantPlan

def devices_view(request):
    plantGroups = PlantGroup.objects.all()
    tankGroups = TankGroup.objects.all()
    climateGroups = ClimateGroup.objects.all()
    context = {
        'plantGroups': plantGroups,
        'tankGroups': tankGroups,
        'climateGroups': climateGroups
    }
    return render(request, 'supplyu95overview.html', context)

def plant_plan_view(request):
    plantGroups = PlantGroup.objects.all()
    tankGroups = TankGroup.objects.all()
    climateGroups = ClimateGroup.objects.all()
    plantPlans = PlantPlan.objects.all()
    context = {
        'plantPlans': plantPlans,
        'plantGroups': plantGroups,
        'tankGroups': tankGroups,
        'climateGroups': climateGroups
    }
    return render(request, 'supplyu95plan.html', context)
from django.shortcuts import render
from .models import Device, PlantGroup, TankGroup, ClimateGroup

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
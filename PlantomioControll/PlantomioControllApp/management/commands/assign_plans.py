from django.core.management.base import BaseCommand
from PlantomioControllApp.models import Device, PlantGroup, TankGroup, ClimateGroup, PlantPlan, PlanValue

class Command(BaseCommand):
    help = 'Assigns existing devices to their respective groups'

    def handle(self, *args, **kwargs):
        values = PlanValue.objects.all()
        for value in values:
            plan, created = PlantPlan.objects.get_or_create(id=value.planId)
            
            plan.values.add(value)
            self.stdout.write(self.style.SUCCESS(f'Value {value.planId} added to plan {plan.id}'))

       
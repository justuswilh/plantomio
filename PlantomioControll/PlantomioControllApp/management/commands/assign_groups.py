from django.core.management.base import BaseCommand
from PlantomioControllApp.models import Device, PlantGroup, TankGroup, ClimateGroup

class Command(BaseCommand):
    help = 'Assigns existing devices to their respective groups'

    def handle(self, *args, **kwargs):
        devices = Device.objects.all()
        for device in devices:
            if device.groupType == 'plant':
                group, created = PlantGroup.objects.get_or_create(number=device.groupNumber)
            elif device.groupType == 'tank':
                group, created = TankGroup.objects.get_or_create(number=device.groupNumber)
            elif device.groupType == 'climate':
                group, created = ClimateGroup.objects.get_or_create(number=device.groupNumber)
            else:
                self.stdout.write(self.style.WARNING(f'Unknown device type for device {device.name}, skipping.'))
                continue  # Unbekannter Gerätetyp, überspringen

            group.devices.add(device)
            self.stdout.write(self.style.SUCCESS(f'Device {device.name} added to group {group.number}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully assigned all devices to their groups'))
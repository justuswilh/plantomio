from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from dirtyfields import DirtyFieldsMixin

class Device(DirtyFieldsMixin, models.Model):
    id = models.CharField(max_length=100, primary_key=True, default='none')
    type = models.CharField(max_length=100, default='none')
    role = models.CharField(max_length=100, default='none')
    name = models.CharField(max_length=100, default='none')
    address = models.CharField(max_length=100, default='none')
    groupType = models.CharField(max_length=100, default='none')
    groupNumber = models.CharField(max_length=100, default='none')

    def __str__(self):
        return f"Id: {self.id}, Type: {self.type}, Role: {self.role}, Name: {self.name}, Address: {self.address}, Group-Type: {self.groupType}, Group-Number: {self.groupNumber}"
    
class PlantGroup(models.Model):
    number = models.CharField(max_length=100, unique=True, default='none')
    name = models.CharField(max_length=100, default='none')
    devices = models.ManyToManyField(Device)
    activPlantPlan = models.CharField(max_length=100, default='none')
    activClimateGroup = models.CharField(max_length=100, default='none')
    activTankGroup = models.CharField(max_length=100, default='none')


    def __str__(self):
        return f"Group Number: {self.number}, Group Name: {self.name}, ActivPlantPlan: {self.activPlantPlan}, ActivClimateGroup: {self.activClimateGroup}, ActivTankGroup: {self.activTankGroup}"
    
class TankGroup(models.Model):
    number = models.CharField(max_length=100, unique=True, default='none')
    name = models.CharField(max_length=100, default='none')
    devices = models.ManyToManyField(Device)

    def __str__(self):
        return f"Group Number: {self.number}, Group Name: {self.name}"
    
class ClimateGroup(models.Model):
    number = models.CharField(max_length=100, unique=True, default='none')
    name = models.CharField(max_length=100, default='none')
    devices = models.ManyToManyField(Device)

    def __str__(self):
        return f"Group Number: {self.number}, Group Name: {self.name}"
    
@receiver(post_save, sender=Device)
def add_device_to_group(sender, instance, created, **kwargs):
    if created or 'groupType' in instance.get_dirty_fields() or 'groupNumber' in instance.get_dirty_fields():
        if instance.groupType == 'plant':
            group, created = PlantGroup.objects.get_or_create(number=instance.groupNumber)
        elif instance.groupType == 'tank':
            group, created = TankGroup.objects.get_or_create(number=instance.groupNumber)
        elif instance.groupType == 'climate':
            group, created = ClimateGroup.objects.get_or_create(number=instance.groupNumber)
        else:
            return  # Unbekannter Gerätetyp, nichts tun

        group.devices.add(instance)
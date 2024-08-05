from django.db import models
from django.db.models.signals import pre_save, post_save
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
    

class PlanValue(DirtyFieldsMixin, models.Model): 
    id = models.AutoField(primary_key=True)    
    planId = models.CharField(max_length=100, default='none')
    week = models.CharField(max_length=100, default='none')
    phase = models.CharField(max_length=100, default='none')
    moistureTarget = models.CharField(max_length=100, default='none')
    moistureMinimum = models.CharField(max_length=100, default='none')
    moistureMaximum = models.CharField(max_length=100, default='none')
    brightnessTarget = models.CharField(max_length=100, default='none')
    brightnessMinimum = models.CharField(max_length=100, default='none')
    brightnessMaximum = models.CharField(max_length=100, default='none')
    lighthoursTarget = models.CharField(max_length=100, default='none')
    lighthoursMinimum = models.CharField(max_length=100, default='none')
    lighthoursMaximum = models.CharField(max_length=100, default='none')
    ecTarget = models.CharField(max_length=100, default='none')
    ecMinimum = models.CharField(max_length=100, default='none')
    ecMaximum = models.CharField(max_length=100, default='none')
    phTarget = models.CharField(max_length=100, default='none')
    phMinimum = models.CharField(max_length=100, default='none')
    phMaximum = models.CharField(max_length=100, default='none')
    temperatureTarget = models.CharField(max_length=100, default='none')
    temperatureMinimum = models.CharField(max_length=100, default='none')
    temperatureMaximum = models.CharField(max_length=100, default='none')
    humidityTarget = models.CharField(max_length=100, default='none')
    humidityMinimum = models.CharField(max_length=100, default='none')
    humidityMaximum = models.CharField(max_length=100, default='none')
    information = models.CharField(max_length=100, default='none')

    def __str__(self):
        return f"PlanId: {self.planId}, Week: {self.week}, Phase: {self.phase}, MoistureTarget: {self.moistureTarget}, MoistureMinimum: {self.moistureMinimum}, MoistureMaximum: {self.moistureMaximum}, BrightnessTarget: {self.brightnessTarget}, BrightnessMinimum: {self.brightnessMinimum}, BrightnessMaximum: {self.brightnessMaximum}, LighthoursTarget: {self.lighthoursTarget}, LighthoursMinimum: {self.lighthoursMinimum}, LighthoursMaximum: {self.lighthoursMaximum}, EcTarget: {self.ecTarget}, EcMinimum: {self.ecMinimum}, EcMaximum: {self.ecMaximum}, PhTarget: {self.phTarget}, PhMinimum: {self.phMinimum}, PhMaximum: {self.phMaximum}, TemperatureTarget: {self.temperatureTarget}, TemperatureMinimum: {self.temperatureMinimum}, TemperatureMaximum: {self.temperatureMaximum}, HumidityTarget: {self.humidityTarget}, HumidityMinimum: {self.humidityMinimum}, HumidityMaximum: {self.humidityMaximum}, Information: {self.information}"

class PlantPlan(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default='none')
    plant = models.CharField(max_length=100, default='none')
    name = models.CharField(max_length=100, default='none')
    weeks = models.CharField(max_length=100, default='none')
    values = models.ManyToManyField(PlanValue)



    def __str__(self):
        return f"Id: {self.id}, Plant: {self.plant}, Name: {self.name}, Weeks: {self.weeks}"


@receiver(pre_save, sender=Device)
def store_old_group_info(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Device.objects.get(pk=instance.pk)
        instance._old_group_type = old_instance.groupType
        instance._old_group_number = old_instance.groupNumber
    else:
        instance._old_group_type = None
        instance._old_group_number = None

@receiver(post_save, sender=Device)
def add_device_to_group(sender, instance, created, **kwargs):
    if created or 'groupType' in instance.get_dirty_fields() or 'groupNumber' in instance.get_dirty_fields():
        # Entferne das Gerät aus der alten Gruppe, falls vorhanden
        if not created and instance._old_group_type and instance._old_group_number:
            if instance._old_group_type == 'plant':
                old_group = PlantGroup.objects.get(number=instance._old_group_number)
            elif instance._old_group_type == 'tank':
                old_group = TankGroup.objects.get(number=instance._old_group_number)
            elif instance._old_group_type == 'climate':
                old_group = ClimateGroup.objects.get(number=instance._old_group_number)
            else:
                old_group = None

            if old_group:
                old_group.devices.remove(instance)

        # Füge das Gerät zur neuen Gruppe hinzu
        if instance.groupType == 'plant':
            group, created = PlantGroup.objects.get_or_create(number=instance.groupNumber)
        elif instance.groupType == 'tank':
            group, created = TankGroup.objects.get_or_create(number=instance.groupNumber)
        elif instance.groupType == 'climate':
            group, created = ClimateGroup.objects.get_or_create(number=instance.groupNumber)
        else:
            return  # Unbekannter Gerätetyp, nichts tun

        group.devices.add(instance)


@receiver(pre_save, sender=PlanValue)
def store_old_plan_id(sender, instance, **kwargs):
    if instance.pk:
        instance._old_plan_id = PlanValue.objects.get(pk=instance.pk).planId
    else:
        instance._old_plan_id = None

@receiver(post_save, sender=PlanValue)
def add_value_to_plantPlan(sender, instance, created, **kwargs):
    if created or 'planId' in instance.get_dirty_fields():
        if not created and instance._old_plan_id and instance._old_plan_id != instance.planId:
            old_plan = PlantPlan.objects.get(id=instance._old_plan_id)
            old_plan.values.remove(instance)
        
        plan, created = PlantPlan.objects.get_or_create(id=instance.planId)
        plan.values.add(instance)
    else:
        return  # Unbekannter Gerätetyp, nichts tun
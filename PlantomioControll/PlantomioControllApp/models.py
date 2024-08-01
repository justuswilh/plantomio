from django.db import models

class Devices(models.Model):
    DeviceID = models.CharField(max_length=200)
    DeviceName = models.CharField(max_length=200)
    DeviceType = models.CharField(max_length=200)
    DeviceAddress = models.CharField(max_length=200)
    DeviceGroup = models.CharField(max_length=200)

    def __str__(self):
        return self.DeviceID, self.DeviceName, self.DeviceType, self.DeviceAddress, self.DeviceGroup
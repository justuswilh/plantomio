from django.shortcuts import render
from .models import Devices

def devices_view(request):
    devices = Devices.objects.all()  # Alle Geräte abfragen
    device_data = {
        'DeviceID': [device.DeviceID for device in devices],
        'DeviceName': [device.DeviceName for device in devices],
        'DeviceType': [device.DeviceType for device in devices],
        'DeviceAddress': [device.DeviceAddress for device in devices],
        'DeviceGroup': [device.DeviceGroup for device in devices],
    }
    return render(request, 'supplyu95overview.html', device_data)
# Generated by Django 5.0.7 on 2024-08-02 17:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("PlantomioControllApp", "0005_groupdevice_groups_groupdevice_group"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="devices",
            name="device_id",
        ),
    ]
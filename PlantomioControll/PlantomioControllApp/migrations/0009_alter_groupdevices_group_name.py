# Generated by Django 5.0.7 on 2024-08-02 17:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "PlantomioControllApp",
            "0008_remove_groupdevices_device_remove_groupdevices_group_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="groupdevices",
            name="group_name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
# Generated by Django 5.0.7 on 2024-08-02 20:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "PlantomioControllApp",
            "0015_alter_plantgroups_devices_climategroups_tankgroups",
        ),
    ]

    operations = [
        migrations.RenameModel(
            old_name="PlantGroups",
            new_name="ClimateGroup",
        ),
        migrations.RenameModel(
            old_name="TankGroups",
            new_name="TankGroup",
        ),
        migrations.RenameModel(
            old_name="Devices",
            new_name="Device",
        ),
        migrations.CreateModel(
            name="PlantGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "group_number",
                    models.CharField(default="none", max_length=100, unique=True),
                ),
                ("group_name", models.CharField(default="none", max_length=100)),
                ("devices", models.ManyToManyField(to="PlantomioControllApp.device")),
            ],
        ),
        migrations.DeleteModel(
            name="ClimateGroups",
        ),
    ]
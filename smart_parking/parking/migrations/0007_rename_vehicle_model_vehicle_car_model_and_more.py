# Generated by Django 5.2 on 2025-04-12 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0006_rename_owner_name_vehicle_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='vehicle_model',
            new_name='car_model',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='plate_number',
            new_name='license_plate',
        ),
    ]

# Generated by Django 4.2.2 on 2023-06-24 13:07

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_rename_sourcedestination_vessel_destinationport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vessel',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=api.models.generate_file_path),
        ),
        migrations.AlterField(
            model_name='vessel',
            name='owner',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='vessel',
            name='ownerNumber',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]

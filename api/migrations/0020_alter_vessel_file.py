# Generated by Django 4.2.2 on 2023-08-01 13:20

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_alter_launch_number_alter_vessel_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vessel',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=api.models.generate_file_path),
        ),
    ]
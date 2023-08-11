# Generated by Django 4.2.2 on 2023-08-11 21:37

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_vesselbooking_company_alter_vessel_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vessel',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=api.models.generate_file_path),
        ),
        migrations.AlterField(
            model_name='vesselbooking',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]

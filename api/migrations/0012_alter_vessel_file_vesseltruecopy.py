# Generated by Django 4.2.2 on 2023-06-27 13:33

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0011_alter_vessel_file_vesselmanifest_vesselattestation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vessel',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=api.models.generate_file_path),
        ),
        migrations.CreateModel(
            name='VesselTrueCopy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('file', models.FileField(blank=True, null=True, upload_to=api.models.generate_file_path)),
                ('note', models.TextField(blank=True, null=True)),
                ('done_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vessel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.vessel')),
            ],
        ),
    ]

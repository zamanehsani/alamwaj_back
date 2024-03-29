# Generated by Django 4.2.2 on 2023-08-13 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_hs_codes_alter_vessel_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=80, null=True)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('logo', models.FileField(blank=True, null=True, upload_to='company')),
                ('trn', models.CharField(blank=True, max_length=50, null=True)),
                ('tel', models.CharField(blank=True, max_length=15, null=True)),
                ('mob', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('pob', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]

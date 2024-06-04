# Generated by Django 5.0.6 on 2024-05-27 15:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuideTMCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='address',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_configuration',
            field=models.CharField(max_length=256),
        ),
        migrations.CreateModel(
            name='TechnicalMaintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TM_date', models.DateField()),
                ('TM_operating_hours', models.FloatField(max_length=64)),
                ('TM_invoice', models.CharField(max_length=64)),
                ('TM_invoice_date', models.DateField()),
                ('TM_responsible_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.guidetmcompany')),
                ('TM_service_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TM_service_company', to='mainApp.vehicle')),
                ('TM_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.guidetm')),
                ('TM_vehicle_SN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TM_vehicle_SN', to='mainApp.vehicle')),
            ],
        ),
    ]

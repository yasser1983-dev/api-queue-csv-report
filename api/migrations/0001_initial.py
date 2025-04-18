# Generated by Django 5.2 on 2025-04-08 04:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TASMSMAESTRO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date_report', models.DateField()),
            ],
            options={
                'db_table': 'TA_SMS_MAESTRO',
            },
        ),
        migrations.CreateModel(
            name='TASMSDETALLE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('receiver', models.CharField(max_length=20)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='api.tasmsmaestro')),
            ],
            options={
                'db_table': 'TA_SMS_DETALLE',
            },
        ),
    ]

# Generated by Django 3.2.20 on 2024-01-04 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_receipt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receipt',
            name='date',
        ),
        migrations.RemoveField(
            model_name='receipt',
            name='vehicle_no',
        ),
    ]

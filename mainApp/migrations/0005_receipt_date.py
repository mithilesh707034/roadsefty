# Generated by Django 3.2.20 on 2024-01-04 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0004_auto_20240105_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='date',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]

# Generated by Django 3.2.20 on 2024-02-29 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0009_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='branch_email',
            field=models.EmailField(blank=True, default=1, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='receipt',
            name='employee_email',
            field=models.EmailField(blank=True, default=1, max_length=254, null=True),
        ),
    ]

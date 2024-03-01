# Generated by Django 3.2.20 on 2024-02-29 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0008_alter_receipt_shift_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('email', models.EmailField(blank=True, default='', max_length=254, null=True)),
                ('password', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('address', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
        ),
    ]
from django.db import models

class Vehicle(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,default="",null=True,blank=True)
    slug=models.CharField(max_length=100,default="",null=True,blank=True)


class Receipt(models.Model):
    id=models.AutoField(primary_key=True)
    operator_class=models.CharField(max_length=100,default="",null=True,blank=True)
    amount=models.CharField(max_length=100,default="",null=True,blank=True)
    date=models.CharField(max_length=100,default="",null=True,blank=True)
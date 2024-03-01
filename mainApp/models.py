from django.db import models

class Vehicle(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,default="",null=True,blank=True)
    slug=models.CharField(max_length=100,default="",null=True,blank=True)
    price=models.IntegerField(default=0,null=True,blank=True)


class Receipt(models.Model):
    id=models.AutoField(primary_key=True)
    operator_class=models.CharField(max_length=100,default="",null=True,blank=True)
    vehicle_number=models.CharField(max_length=100,default="",null=True,blank=True)
    amount=models.CharField(max_length=100,default="",null=True,blank=True)
    date=models.CharField(max_length=100,default="",null=True,blank=True)
    shift_name=models.CharField(max_length=10,default=1,null=True,blank=True)
    branch_email=models.EmailField(default=1,null=True,blank=True)
    employee_email=models.EmailField(default=1,null=True,blank=True)

class Branch(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,default="",null=True,blank=True)
    email=models.EmailField(default="",null=True,blank=True)
    password=models.CharField(max_length=30,default='',null=True,blank=True)
    address=models.CharField(max_length=100,default="",null=True,blank=True)


class Employee(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,default="",null=True,blank=True)
    email=models.EmailField(default="",null=True,blank=True)
    password=models.CharField(max_length=30,default='',null=True,blank=True)
    address=models.CharField(max_length=100,default="",null=True,blank=True)
    branch_email=models.EmailField(default=1,null=True,blank=True)
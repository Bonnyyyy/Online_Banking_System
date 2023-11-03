from django.db import models
from django.core.validators import MaxValueValidator
from datetime import date
today=date.today()
# Create your models here.
class User_table(models.Model):
    First_name=models.CharField(max_length=50)
    Middle_name=models.CharField(max_length=50)
    Last_name=models.CharField(max_length=50)
    Gender=models.CharField(max_length=20)
    Dob=models.DateField()
    Ph_no=models.IntegerField()
    Email=models.EmailField()
    Address=models.CharField(max_length=200)
    City=models.CharField(max_length=30)
    District=models.CharField(max_length=50)
    State=models.CharField(max_length=30)
    Pin=models.IntegerField()
    Aadhaar=models.IntegerField()
    PAN=models.CharField(max_length=15)
    passport=models.CharField(max_length=20)
    pic=models.ImageField(upload_to='profile/',blank=True, null=True)
    username=models.CharField(max_length=10)
    password=models.CharField(max_length=15)
    mpin=models.IntegerField(validators=[MaxValueValidator(9999)])
    question=models.CharField(max_length=60)
    answer=models.CharField(max_length=20)
    ac_no=models.CharField(max_length=15)
    balance=models.IntegerField(default=0)
    flag=models.IntegerField(default=0)
    card=models.IntegerField(default=0)
    cvv=models.IntegerField(default=0)
    class Meta:
        db_table="User_table"

class Transection(models.Model):
    fac_no=models.CharField(max_length=15)
    tac_no=models.CharField(max_length=15)
    date=models.DateField(default=today)
    reference=models.CharField(max_length=200)
    tr_id=models.CharField(max_length=30)
    credit=models.IntegerField(default=0)
    debit=models.IntegerField(default=0)
    balance=models.IntegerField(default=0)
    class Meta:
        db_table = "Transection"

class AdminDb(models.Model):
    name=models.CharField(max_length=50)
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)
    class Meta:
        db_table = "AdminDb"
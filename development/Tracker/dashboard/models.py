from django.db import models
from django.contrib.auth.models import User
from loginApp.models import Organization
# Create your models here.

class FamilyModel(models.Model):
    family_ID = models.CharField(unique=True,blank=False,max_length=8)
    phone_number = models.CharField(unique=True,blank=False,max_length=10)
    residential_address = models.TextField(max_length=300,blank=False,default='none')
    created_by_org = models.ForeignKey(User,on_delete=models.CASCADE,default=8)
    in_public_domain = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.family_ID

class memberOfaFamily(models.Model):
    name = models.CharField(max_length=200,null=False)
    aadhar = models.CharField(max_length=12,null=False,unique=True)
    age = models.PositiveSmallIntegerField(null=False)
    gender = models.CharField(max_length=1,null=False)
    belongs_to = models.ForeignKey(FamilyModel,on_delete=models.CASCADE)
    def __str__(self):
        return self.aadhar
    
class Benefit(models.Model):
    given_to = models.ForeignKey(FamilyModel,on_delete=models.CASCADE)
    given_by = models.ForeignKey(Organization,on_delete=models.CASCADE,default=1)
    amount = models.DecimalField(max_digits=8,decimal_places=2,null=False)
    transaction_ID = models.CharField(max_length=18,null=False)
    purpose = models.TextField(null=False)
    date = models.DateField(auto_now_add=True)

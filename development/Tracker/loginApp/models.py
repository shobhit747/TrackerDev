from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Organization(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    organizationName = models.CharField(max_length = 200,blank=False)
    localAddress = models.TextField(blank=False,null=False,default='none')
    aboutOrg = models.TextField(blank=False,null=False,default='none')
    mobile = models.CharField(max_length=10,blank=False,null=False,default='none')
    



    def __str__(self):
        return self.organizationName
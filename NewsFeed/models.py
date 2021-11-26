from django.db import models
from django.conf import settings

class Countries(models.Model):
    countryName= models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    
class Sources(models.Model):
    sourceName=models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    
class Keywords(models.Model):
    keyword=models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)

class Mapper(models.Model):
    itemName =models.CharField(max_length=100)
    selecteddata =models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)


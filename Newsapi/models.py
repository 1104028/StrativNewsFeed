from django.db import models

class NewsItem(models.Model):
    title = models.CharField(max_length=300)
    source = models.CharField(max_length=200)
    url = models.CharField(max_length=1000)
    imageurl = models.CharField(max_length=1000,null=True)
    country =models.CharField(max_length=100)

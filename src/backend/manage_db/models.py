from django.db import models


class Data(models.Model):
    ticker = models.CharField(unique=True,primary_key=True,max_length=20)
    last_updated = models.DateTimeField()
    file_path = models.CharField(max_length=256)
    

from django.db import models


class Data(models.Model):
    ticker = models.CharField(unique=True,primary_key=True,max_length=20)
    last_updated = models.DateTimeField()
    file_path = models.CharField(max_length=256)
    last_date = models.DateTimeField()
    url_link = models.CharField(max_length=256)
    
    
    def update(self):
        """
        Update the file with remote copy.
        """
        pass
    
    
    def download(self):
        """
        Download the remote copy.
        """
        pass
        
    

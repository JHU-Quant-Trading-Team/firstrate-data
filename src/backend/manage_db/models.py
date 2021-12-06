from datetime import date
from django.db import models
from django.utils import timezone
import os


class Data(models.Model):
    ticker = models.CharField(unique=True,primary_key=True,max_length=20)
    last_updated = models.DateTimeField()
    file_path = models.CharField(max_length=256, default='')
    download_link = models.CharField(max_length=256, default='')
    update_link = models.CharField(max_length=256, default='')
    
    
    def update(self):
        """
        Update the file with remote copy.
        """
        pass
    
    
    def get_remote_time(self):
        """
        Gets the last datetime of the remote data.
        """
        # Download remote updated data
        
        # Get the remote time 
        pass
    
    
    def __get_time(self, file_path):
        with open(file_path, "rb") as file:
            # Go to the end of the file before the last break-line
            file.seek(-2, os.SEEK_END) 
            # Keep reading backward until you find the next break-line
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR) 
            last_line = file.readline().decode()
            return timezone.datetime.strptime(last_line[:last_line.find(',')], "%Y-%m-%d %H:%M:%S")
    
    
    def get_local_time(self):
        """
        Gets the last datetime of the local data.
        """

        return self.__get_time(self.file_path)
        
    
    
    def download(self):
        """
        Download the remote copy.
        """
        pass
        
    

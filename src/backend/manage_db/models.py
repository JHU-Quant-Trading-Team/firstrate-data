from datetime import date
from django.db import models
from django.utils import timezone
import urllib.request
import os
import zipfile
import shutil



class DataBundle(models.Model):
    name = models.CharField(primary_key=True, max_length=16)
    download_link = models.CharField(max_length=256, default="")
    update_link = models.CharField(max_length=256, default="")
    root_path = models.CharField(max_length=256, default="")
    
    
    def download(self):
        """
        Download the remote copy.
        """
        # Create folder to extract remote data to
        if not os.path.exists(self.root_path):
            os.makedirs(self.root_path)
        
        # Download remote data
        zip_file_name = f'{self.root_path}temp.zip'
        urllib.request.urlretrieve(self.update_link, zip_file_name)
        
        # Unzip remote data
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            zip_ref.extractall(f'{self.root_path}')
            
        # Remove zip file
        os.remove(zip_file_name)
    
    
    def update(self):
        """
        Update the file with remote copy.
        """
        pass
    
    
    def get_remote_time(self):
        """
        Gets the last datetime of the remote data.
        """
        
        # Create temporary folder to extract remote data to
        if not os.path.exists('temp/'):
            os.makedirs('temp/')
        
        # Download remote updated data
        urllib.request.urlretrieve(self.update_link, 'temp/temp.zip')
        
        # Unzip temp data
        with zipfile.ZipFile('temp/temp.zip', 'r') as zip_ref:
            zip_ref.extractall('temp/')
        
        # Get the remote time
        ## Get all data objects related to this bundle
        data_objects = Data.objects.filter(bundle=self)
        
        ## Get times from data files
        times = [Data.__get_time(f'temp/{data.file_name}') for data in data_objects]
        
        ## Get the most recent time
        remote_time = max(times)
        
        # Delete temporary folder
        shutil.rmtree('temp/')
        
        return remote_time
    
    
    def get_local_time(self):
        """
        Gets the last datetime of the local data.
        """
        # Get all data objects related to this bundle
        data_objects = Data.objects.filter(bundle=self)
        
        # Get all the local times of the files
        times = [Data.__get_time(f'{self.root_path}/{data.file_name}') for data in data_objects]

        # Return the most recent time
        return max(times)
    
class Data(models.Model):
    ticker = models.CharField(unique=True,primary_key=True,max_length=20)
    file_name = models.CharField(max_length=256, default="")
    bundle = models.ForeignKey(DataBundle, on_delete=models.CASCADE)
    
    
    @staticmethod
    def __get_time(file_path):
        with open(file_path, "rb") as file:
            # Go to the end of the file before the last break-line
            file.seek(-2, os.SEEK_END) 
            # Keep reading backward until you find the next break-line
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR) 
            last_line = file.readline().decode()
            return timezone.datetime.strptime(last_line[:last_line.find(',')], "%Y-%m-%d %H:%M:%S")
    
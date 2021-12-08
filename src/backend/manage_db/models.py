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
        zip_file_name = self.root_path + 'temp.zip'
        urllib.request.urlretrieve(self.update_link, zip_file_name)
        
        # Unzip remote data
        with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
            zip_ref.extractall(self.root_path)
            
        # Remove zip file
        os.remove(zip_file_name)
    
    
    def update(self):
        """
        Update the files with remote copy if there are updates.
        """
        # Create temporary folder to extract remote data to
        temp_root = self.root_path + 'temp/'
        if not os.path.exists(temp_root):
            os.makedirs(temp_root)
            
        # Download remote updated data
        urllib.request.urlretrieve(self.update_link, temp_root + '/temp.zip')
        
        # Unzip temp data
        with zipfile.ZipFile(temp_root + '/temp.zip', 'r') as zip_ref:
            zip_ref.extractall(temp_root)
        
        # Update each object
        ## Get all data objects related to this bundle
        data_objects = Data.objects.filter(bundle=self)
        
        ## Use the Data update method to update each file
        ## This will do checking and only add lines if they don't exist already
        for data in data_objects:
            data.update(temp_root + data.file_name)
        
        # Delete temporary folder
        shutil.rmtree(temp_root)


class Data(models.Model):
    ticker = models.CharField(unique=True,primary_key=True,max_length=20)
    file_name = models.CharField(max_length=256, default="")
    bundle = models.ForeignKey(DataBundle, on_delete=models.CASCADE)
    
    
    def update(self, remote_file: str):
        """
        Update the file with remote copy.
        """
        # Determine the most recent times on both files
        local_file = self.bundle.root_path + self.file_name
        local_time = Data.__get_time(local_file)
        remote_time = Data.__get_time(remote_file)
        
        # If there are differences
        if local_time < remote_time:
            # Find the lines not present in the local file
            lines_to_write = []
            with open(remote_file, 'r') as f:
                remote_lines = reversed(f.readlines()) # update files are small, so should not be an issue
                for line in remote_lines:
                    time = timezone.datetime.strptime(line[:line.find(',')], "%Y-%m-%d %H:%M:%S")
                    
                    if time != local_time:
                        lines_to_write.append(line)
            lines_to_write = reversed(lines_to_write)
            
            # Write lines to local file
            with open(local_file, 'w') as f:
                f.writelines(lines_to_write)
            
    
    @staticmethod
    def __get_time(file_path: str):
        """
        Get the most recent time in a csv file.

        Args:
            file_path (str): file path

        Returns:
            datetime
        """
        with open(file_path, "rb") as f:
            # Go to the end of the file before the last break-line
            f.seek(-2, os.SEEK_END) 
            # Keep reading backward until you find the next break-line
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR) 
            last_line = f.readline().decode()
            return timezone.datetime.strptime(last_line[:last_line.find(',')], "%Y-%m-%d %H:%M:%S")

    
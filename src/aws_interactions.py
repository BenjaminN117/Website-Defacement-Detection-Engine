'''
Product: Ineractions with AWS
Description: Provides the processes for interacting with S3 and SNS
Author: Benjamin Norman 2023
'''

from env import *

import boto3
import logging
import os
from cloudpathlib import CloudPath

'''
- Download any public facing web files in a single project.
- Store them in a temp folder on the container
- Return a list of websites that need to be fetched based on these files
- When there are changes detected, send a notif through SNS
'''

class s3_interactions():
    
    s3Client: object
    s3Resource: object
    
    def __init__(self):
        self.s3Client = boto3.client('s3')
        self.s3Resource = boto3.resource('s3')
        
    def data_download(self):
        # WORKING
        
        '''
        Download the production code from the S3 bucket
        - Search for all of the prefixes in the location
        - Download all of the files into a predefined location
        '''
        
        downloadLocation = CloudPath(WEBSITES_LOCATION)
        
        os.makedirs(PRODUCTION_WEBSITES_DOWNLOAD_LOCATION, exist_ok=True)
        
        downloadLocation.download_to(PRODUCTION_WEBSITES_DOWNLOAD_LOCATION)
        
    def data_upload(self, filename):
        '''
        Used to upload log files and JSON data
        
        - Only log files should be used when an error occurs in the program
          and JSON files should be uploaded when differences are found
        '''
        with open(filename, 'rb') as data:
            if filename.startswith("LOG"):
                self.s3.upload_fileobj(data, BUCKET_NAME, 'mykey')
            else:
                self.s3.upload_fileobj(data, BUCKET_NAME, 'mykey')
    
    
    
class sns_interactions():
    def __init__(self):
        self.sesClient = boto3.client('ses')
    
    def notifications(self):
        '''
        Send a notification through SNS from when errors occur
        or when issues arise
        
        Publishes to an existing AWS topic that needs to be configured prior to deployment
        
        - The notification should include the the S3 object address of the JSON file
        - If a log file is created, then the address of the log file should be included
        '''
        pass
    
# Testing only
if __name__ == "__main__":
    inst = s3_interactions()
    inst.data_download()
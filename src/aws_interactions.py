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
        
        os.makedirs(f"{PRODUCTION_WEBSITES_DOWNLOAD_LOCATION}Data/Production_Data", exist_ok=True)
        
        downloadLocation.download_to(f"{PRODUCTION_WEBSITES_DOWNLOAD_LOCATION}/Data/Production_Data/")
        
    def data_upload(self):
        '''
        Used to upload log files and JSON data
        
        - Only log files should be used when an error occurs in the program
          and JSON files should be uploaded when differences are found
        '''
        with open('filename', 'rb') as data:
            self.s3.upload_fileobj(data, 'mybucket', 'mykey')
        pass
    
    def domain_list_creation(self):
        # Working
        
        '''
        Compile a list of all websites that need to be fetched
        
        - The domain names should be the name of the prefix e.g. google.com
        - Collect the domain names and add them to a list along with the https:// formatting. This
        makes the assumption that all websites being tested are HTTPS (Should be an ok assumption to make
        in 2023)
        - List should be fetched from the Container file system, not S3, to prevent unneccessary requests to S3
        '''
        domainJSON = {"domains":[]}
        
        for domainName in os.listdir(f"{PRODUCTION_WEBSITES_DOWNLOAD_LOCATION}Data/Production_Data"):
            temp = {domainName:[]}
            for fileName in os.listdir(f"{PRODUCTION_WEBSITES_DOWNLOAD_LOCATION}Data/Production_Data/{domainName}"):
                temp[domainName].append(fileName)
            domainJSON["domains"].append(temp)
        
        return domainJSON
    
class sns_interactions():
    def __init__(self):
        pass
    
    def notifications(self):
        '''
        Send a notification through SNS from when errors occur
        or when issues arise
        
        - The notification should include the the S3 object address of the JSON file
        - If a log file is created, then the address of the log file should be included
        '''
        pass
    
# Testing only
if __name__ == "__main__":
    inst = s3_interactions()
    inst.data_download()
    print(inst.domain_list_creation())
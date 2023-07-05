'''
Product: Interactions with AWS
Description: Provides the processes for interacting with S3 and SNS
Author: Benjamin Norman 2023
'''

from env import *

import boto3
from botocore.exceptions import ClientError
import os
from cloudpathlib import CloudPath

class s3_interactions():
    
    s3Client: object
    s3Resource: object
    
    def __init__(self, loggerObj):
        self.s3Client = boto3.client('s3')
        self.s3Resource = boto3.resource('s3')
        self.logger = loggerObj
        
    def data_download(self):
        '''
        Download the production code from the S3 bucket
        - Search for all of the prefixes in the location
        - Download all of the files into a predefined location
        '''
        try:
            downloadLocation = CloudPath(WEBSITES_LOCATION)
        
            os.makedirs(PRODUCTION_WEBSITES_DOWNLOAD_LOCATION, exist_ok=True)
        
            downloadLocation.download_to(PRODUCTION_WEBSITES_DOWNLOAD_LOCATION)
        except Exception as error:
            self.logger.critical(f"Unable to download production data - {error}")
    def data_upload(self, filename):
        '''
        Used to upload log files and JSON data
        
        - Only log files should be used when an error occurs in the program
          and JSON files should be uploaded when differences are found
        '''
        try:
            response = self.s3Client.upload_file(filename, BUCKET_NAME, f"{LOG_FILE_LOCATION}{filename}")
        except ClientError as e:
            return e
        return True
    
class sns_interactions():
    def __init__(self, loggerObj):
        self.sesClient = boto3.client('ses')
        self.logger = loggerObj
    def notifications(self):
        '''
        Send a notification through SNS from when errors occur
        or when issues arise
        
        Publishes to an existing AWS topic that needs to be configured prior to deployment
        
        - The notification should include the the S3 object address of the JSON file
        - If a log file is created, then the address of the log file should be included
        '''
        pass
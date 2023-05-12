'''
Product: Ineractions with AWS
Description: Provides the processes for interacting with S3 and SNS
Author: Benjamin Norman 2023
'''

import boto3
import logging

'''
- Download any public facing web files in a single project.
- Store them in a temp folder on the container
- Return a list of websites that need to be fetched based on these files
- When there are changes detected, send a notif through SNS
'''

class s3_interactions():
    
    s3: object
    
    def __init__(self):
        self.s3 = boto3.client('s3')
    
    def data_download(self):
        '''
        Download the known good code from the S3 bucket
        - Search for all of the prefixes in the location
        - Download all of the files into a predefined location
        '''
        
        for my_bucket_object in self.s3.objects.all():
            print(my_bucket_object)
            
    def data_upload(self):
        '''
        Used to upload log files and JSON data
        
        - Only log files should be used when an error occurs in the program
          and JSON files should be uploaded when differences are found
        '''
        with open('filename', 'rb') as data:
            self.s3.upload_fileobj(data, 'mybucket', 'mykey')
        pass
    
    def list_creation(self):
        '''
        Compile a list of all websites that need to be fetched
        
        - The domain names should be the name of the bucket e.g. google.com
        - Collect the domain names and add them to a list along with the https:// formatting. This
        makes the assumption that all websites being tested are HTTPS (Should be an ok assumption to make
        in 2023)
        '''
        pass
    
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
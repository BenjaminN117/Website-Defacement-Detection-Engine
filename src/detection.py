'''
Product:
Description:
Author: Benjamin Norman 2023
'''

import logging
import os
import requests
import json
import shutil

from pywebcopy import save_web_page

from env import *
from aws_interactions import s3_interactions, sns_interactions

class website_detection():
    # Import a logging object as well when that stage is next up
    def __init__(self):
        self.S3Interactions = s3_interactions()
        self.SNSInteractions = sns_interactions()

    def web_fetcher(self):
        '''
        - While doing the web fetching, also do a DNS lookup to ensure the IP address of the website is
          stored, just in case it is part of a cluster
        - If the website has mulitple pages, download them all, these names should then be based off of the
          known good code folder. e.g. https://somethingFishy.com/index.html
        '''
        
        '''
        Fetches the website data from the listed
        websites
        '''
        
        builtURL = ""
        domainList = self.domain_list_creation()
        
        os.makedirs("Data/Live_Data", exist_ok=True)
        
        # Fetch the website data for HTTPS to start with and then HTTP if not exists
        
        for domain in domainList["domains"]:
            key = list(domain.keys())[0]
            print(key)
            os.makedirs(f"Data/Live_Data/{key}", exist_ok=True)
            download_folder = f'Data/Live_Data/{key}'   
            kwargs = {'bypass_robots': True}
            
            webFiles = self.file_indexing(f"Data/Production_Data/{key}")
            
            self.data_cleaning(webFiles=webFiles)
            
            print(webFiles)
            
            # for subdomain in webFiles:
                
            #     try:
            #         try:
            #             builtURL = f"https://{key}/{subdomain}"
            #             print(builtURL)
            #             #save_web_page(builtURL, download_folder, **kwargs)
            #         except requests.exceptions.SSLError:
            #             builtURL = f"http://{key}/{subdomain}"
            #             print(builtURL)
            #             #save_web_page(builtURL, download_folder, **kwargs)
            #             os.removedirs(f"Data/Live_Data/{key}/https_{key}")
            #     except Exception as err:
            #         print(f"URL NOT FOUND {err}")
            #         shutil.rmtree(f"Data/Live_Data/{key}", ignore_errors=True)
                
            #     # for subdomain in domain[key]:
            #     #     builtURL = f"https://{key}/{subdomain}"
                
            # print(builtURL)
    
    def data_cleaning(self, webFiles):
        
        # Private function
        
        # Dependancy for web_fetcher
        
        '''
        Removes the comments added by the pywebcopy module that could interfere
        with the detection process.
        
        Needs to be run on every .html file as this is what it effects
        
        '''
        for x in webFiles:
            if x.endswith(".html"):
                with open(x, "r") as file:
                    lines = file.readlines()

                # Filter out the lines to be removed
                lines_to_remove = [2, 3, 4, 5, 6]  # Example: remove lines 2, 4, and 7
                filtered_lines = [line for i, line in enumerate(lines) if i+1 not in lines_to_remove]

                # Open the output file in write mode
                with open(x, "w") as file:
                    file.writelines(filtered_lines)
                
    def file_indexing(self, domainFile):
        
        # Private function
        # Dependancy for web_fetcher
        
        webFiles = []
        
        '''
        Look for each file in the directory and record it
        '''
        
        dir_entries = os.scandir(domainFile)
        for entry in dir_entries:
            if entry.is_file():
                webFiles.append(entry)
        
        return webFiles
    
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
    
    
    def comparison(self):
        
        # Private function
        
        '''
        Compares the known good code to the publicly running
        one
        
        - All data should be exported to a JSON file, if differences are found. If not then it shouldn't be logged.
        '''
        pass
    
    
if __name__ == "__main__":
    inst = website_detection()
    
    inst.web_fetcher()
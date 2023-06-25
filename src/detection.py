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
        #domainList = self.domain_list_creation(PRODUCTION_WEBSITES_DOWNLOAD_LOCATION)
        
        os.makedirs("Data/Live_Data", exist_ok=True)
        
        # Fetch the website data for HTTPS to start with and then HTTP if not exists
        
        print(domainList)
        
        for domain in domainList["domains"]:
            key = list(domain.keys())[0]
            print(key)
            os.makedirs(f"Data/Live_Data/{key}", exist_ok=True)
            download_folder = f'Data/Live_Data/{key}'   
            kwargs = {'bypass_robots': True}
            
            #webFiles = self.file_indexing(f"Data/Production_Data/{key}")
            
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

                lines_to_remove = [2, 3, 4, 5, 6]
                filtered_lines = [line for i, line in enumerate(lines) if i+1 not in lines_to_remove]
                
                for i, line in enumerate(filtered_lines):
                    if line.startswith('-->'):
                        newline = line.replace("-->", '')
                        filtered_lines[i] = newline

                # Open the output file in write mode
                with open(x, "w") as file:
                    file.writelines(filtered_lines)
    
    def comparison(self):
        
        # Private function
        
        '''
        Compares the known good code to the publicly running
        one
        
        - All data should be exported to a JSON file, if differences are found. If not then it shouldn't be logged.
        
        - if it is a text file like HTML or CSS, then do a line by line comparison. If it is a non
          text file like an image, then do a hash function comparison
        - if the file does not exist in production then add it into the report or filenames that aren't there
        
        '''

        pass
    
    
    def dir_walker(self, targetFilePath):

        domainWalk = {"domains":[]}
        
        # Nested due to no other func needing this.
        def list_search(domainWalk, domainName):
            for item in domainWalk["domains"]:
                if domainName in item.keys():
                    return True
            return False
        
        for path,subdir,files in os.walk(targetFilePath):
            for name in files:    
                
                strippedName = os.path.join(path,name).replace(targetFilePath, '')[1:]
                
                strippedPath = strippedName.split('/')
                
                domainName = strippedPath[0]
                fileName = strippedPath[-1]
    
                result = list_search(domainWalk, domainName)
                
                if result == True:
                    for item in domainWalk["domains"]:
                        for key, value in item.items():
                            if key == domainName:
                                value.append({fileName:strippedName})
                elif result == False:
                    domainWalk["domains"].append({domainName:[{fileName:strippedName}]})
                    
        return domainWalk
                

    
if __name__ == "__main__":
    inst = website_detection()
    
    #inst.web_fetcher()
    #inst.dir_walker()
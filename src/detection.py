'''
Product:
Description:
Author: Benjamin Norman 2023
'''

import logging
import os
import requests
import json

from aws_interactions import s3_interactions, sns_interactions

class website_detection():
    def __init__(self):
        pass
    
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
        s3_int = s3_interactions()
        
        builtURL = ""
        domainList = s3_int.domain_list_creation()
        
        os.makedirs("Data/Live_Data", exist_ok=True)
        
        for domain in domainList["domains"]:
            key = list(domain.keys())[0]
            print(key)
            os.makedirs(f"Data/Live_Data/{key}", exist_ok=True)
            for subdomain in domain[key]:
                builtURL = f"https://{key}/{subdomain}"
                
                print(builtURL)
                
        # Fetch the website data based on the files
    
    def comparison(self):
        '''
        Compares the known good code to the publicly running
        one
        
        - All data should be exported to a JSON file, if differences are found. If not then it shouldn't be logged.
        '''
        pass
    
    
if __name__ == "__main__":
    inst = website_detection()
    
    inst.web_fetcher()
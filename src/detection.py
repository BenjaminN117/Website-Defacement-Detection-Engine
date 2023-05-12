'''
Product:
Description:
Author: Benjamin Norman 2023
'''

import logging

class website_detection():
    def __init__(self):
        pass
    
    def load_list(self):
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
        pass
    
    def comparison(self):
        '''
        Compares the known good code to the publicly running
        one
        
        - All data should be exported to a JSON file, if differences are found. If not then it shouldn't be logged.
        '''
        pass
'''
Product: Detection
Description: Detects differences in files provided from the production and live environments
Author: Benjamin Norman 2023
'''
import logging
import json
import hashlib

from env import *
from web_fetch import website_fetcher

class website_detection():
    # Import a logging object as well when that stage is next up
    def __init__(self):
        pass

    def comparison(self, productionDirectoryWalk, liveDirectoryWalk):
        
        # Private function
        
        '''
        Compares the known good code to the publicly running
        one
        
        - All data should be exported to a JSON file, if differences are found. If not then it shouldn't be logged.
        
        - if it is a text file like HTML or CSS, then do a line by line comparison. If it is a non
          text file like an image, then do a hash function comparison
        - if the file does not exist in production then add it into the report or filenames that aren't there
        
        First look at the files in the live directory, compare those to the paths and filenames of the production directory, for every match do a comparison
        and for every difference add it to the output file as an unknown file
        
        '''
        # import the dict of known text file extensions that need comparison and not hashing
        with open("file_extensions.json", "r") as data:
            fileExtensions = json.load(data)
            
        
        for liveItem, prodItem in zip(liveDirectoryWalk["domains"], productionDirectoryWalk["domains"]):
            for liveKey, liveValue, prodKey, prodValue in zip(liveItem.items(), prodItem.items()):
                print(liveKey)
            
        # for item in liveDirectoryWalk["domains"]:
        #     for key, value in item.items():
        #         for x in value:
        #             for nkey, nvalue in x.items():
        #                 print(nkey, nvalue)
                        
        # for item in productionDirectoryWalk["domains"]:
        #     for key, value in item.items():
        #         for x in value:
        #             for nkey, nvalue in x.items():
        #                 print(nkey, nvalue)
                        
                        
        # if ".html" in fileExtensions:
        #     print("true")
        # else:
        #     if hashing("prodFilename") != hashing("liveFileName"):
        #         print("Different Files")
        #     else:
        #         print("SameFiles")
            
    def hashing(self, filePath):
        with open(filePath, 'rb') as f:
            image_data = f.read()
        sha256_hash = hashlib.sha256()
        sha256_hash.update(image_data)
        return sha256_hash.hexdigest()
    
    
if __name__ == "__main__":
    inst = website_detection()
    web = website_fetcher()
    
    productionDirectoryWalk = web.dir_walker(PRODUCTION_WEBSITES_DOWNLOAD_LOCATION)
    liveDirectoryWalk = web.dir_walker(LIVE_WEBSITES_DOWNLOAD_LOCATION)
    
    inst.comparison(productionDirectoryWalk, liveDirectoryWalk)
    
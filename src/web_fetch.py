'''
Product: Web Fetch
Description: Fetches the live website data and stored it in the desired directory
Author: Benjamin Norman 2023
'''
import logging
import os
import re
import requests
import shutil

from pywebcopy import save_website

from env import *

class website_fetcher():
    # Import a logging object as well when that stage is next up
    def __init__(self):
        pass

    def web_fetcher(self, productionDirectoryWalk):
        '''
        - While doing the web fetching, also do a DNS lookup to ensure the IP address of the website is
          stored, just in case it is part of a cluster
        - If the website has mulitple pages, download them all, these names should then be based off of the
          known good code folder. e.g. https://somethingFishy.com/index.html

        Fetches the website data from the listed
        websites
        '''
        builtURL = ""
        
        # Fetch the website data for HTTPS to start with and then HTTP if not exists
        
        for item in productionDirectoryWalk["domains"]:
            for domain, value in item.items():
                download_folder = f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{domain}"
                kwargs = {'bypass_robots': True}
                
                try:
                    try:
                        builtURL = f"https://{domain}"
                        print(builtURL)
                        save_website(builtURL, download_folder, **kwargs)
                        if len(os.listdir(f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{domain}/https_{domain}")) == 0:
                            # Log to the log file
                            shutil.rmtree(f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{domain}")
                        else:
                            self.directory_cleaning(f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{domain}/https_{domain}/{domain}", f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{domain}/")
                            self.directory_cleaning(f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{domain}/https_{domain}", f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{domain}/")

                    except requests.exceptions.SSLError:
                        builtURL = f"http://{domain}"
                        print(builtURL)
                        save_website(builtURL, download_folder, **kwargs)
                        os.removedirs(f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{domain}/https_{domain}")
                        if len(os.listdir(f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{domain}/http_{domain}")) == 0:
                            shutil.rmtree(f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{domain}")
                        else:
                            self.directory_cleaning(f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{domain}/http_{domain}/{domain}", f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{domain}/")
                            self.directory_cleaning(f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{domain}/http_{domain}", f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{domain}/")
                # This is part of the bug
                except Exception as err:
                    print(f"URL NOT FOUND {err}")
                    shutil.rmtree(f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{domain}", ignore_errors=True)

    def directory_cleaning(self, target, destination):
        '''
        Moves all files in a directory back one, then deletes the directory they were in
        '''
        
        for file in os.listdir(target):
            file_path = os.path.join(target, file)
            shutil.move(file_path, destination)
            
        shutil.rmtree(target)
        
    def data_cleaning(self, fileName):
        
        '''
        Removes the comments added by the pywebcopy module that could interfere
        with the detection process.    
        '''
        with open(fileName, "r") as file:
            lines = file.readlines()
            
        # Searches for the lines containing the pattern
        for index, line in enumerate(lines):
            if (line.lstrip().startswith("<!--") or line.lstrip().rstrip().endswith("<!--")) and lines[index+1].lstrip().startswith("* PyWebCopy"):
                print("made it")
                if (re.sub(r"\s+", "", lines[index+4]).lstrip().startswith("*At") or re.sub(r"\s+", "", lines[index+3]).lstrip().startswith("*At")) and (lines[index+5].lstrip().startswith("-->") or lines[index+4].lstrip().startswith("-->")):
                    print(f"Is between lines {index} and {index+6}")
                    if index == 0:
                        print("here")
                        startingNumber = 1
                        headerNumber = 0
                        lineDifference = 5
                    else:
                        startingNumber = index
                        headerNumber = index
                        lineDifference = 6
                    endingNumber = index+6
        
        '''
        Removes the 

        * PyWebCopy Engine [version 7.0.2]
        * Copyright 2020; Raja Tomar
        * File mirrored from [https://angliancreative.com/]
        *At UTC datetime: [2023-06-30 10:04:48.627810]
        
        bit but not the trailing comment
        '''

        try:
            lines_to_remove = list(range(startingNumber+1, endingNumber))
        except NameError as error:
            print(f"No comments identified - {error}")
            return False
        filtered_lines = [line for i, line in enumerate(lines) if i+1 not in lines_to_remove]
        
        for i, line in enumerate(filtered_lines):
            if i == headerNumber:
                newline = line.replace("<!--", '')
                filtered_lines[i] = newline
                
        for i, line in enumerate(filtered_lines):
            if i == endingNumber-lineDifference:
                newline = line.replace("-->", '')
                filtered_lines[i] = newline


        with open(fileName, "w") as file:
                        file.writelines(filtered_lines)
     
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
                
                if not name.startswith("."): # Ignores hidden files
                    strippedName = os.path.join(path,name).replace(targetFilePath, '')[1:]
                else:
                    continue
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
    inst = website_fetcher()
    
    productionDirectoryWalk = inst.dir_walker(PRODUCTION_WEBSITES_DOWNLOAD_LOCATION)
    inst.web_fetcher(productionDirectoryWalk)
    liveDirectoryWalk = inst.dir_walker(LIVE_WEBSITES_DOWNLOAD_LOCATION)
    
    
    # ### Data cleaning ###
    # for item in liveDirectoryWalk["domains"]:
    #     for key, value in item.items():
    #         for x in value:
    #             for nkey, nvalue in x.items():
    #                 try:
    #                     inst.data_cleaning(fileName=f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{nvalue}")
    #                 except UnicodeDecodeError as error:
    #                     print(f"Unicode Error - {error}")
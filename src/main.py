'''
Product:
Description:
Author: Benjamin Norman 2023
'''


from aws_interactions import s3_interactions
from aws_interactions import sns_interactions
from detection import website_detection
from web_fetch import website_fetcher
from env import *

import logging
import argparse
import datetime

class runner():
    def __init__(self) -> None:
        pass

    def generate_logger_file(self, loggerLevel):
        '''
        initiate logger obj
        '''
        currentDateTime = datetime.datetime.now()
        date = datetime.date.today()
        
        logger_name = f"WDDE_{date.year}-{date.month}-{date.day}_"+currentDateTime.strftime("%H:%M:%S_UTC")+".log"
        logging.basicConfig(filename=logger_name,
                    format='%(levelname)s - %(asctime)s: %(message)s',
                    filemode='w')
        logger = logging.getLogger()
        
        if loggerLevel not in ["debug", "info", "warning", "error", "critical"] and loggerLevel != None:
            loggerLevel = LOGGING_LEVEL
            print("Unknown level given, using env")
            if LOGGING_LEVEL not in ["debug", "info", "warning", "error", "critical"] and loggerLevel != None:
                loggerLevel = "info"
                print("Unable to use env value, defaulting to INFO")
                
        if loggerLevel == "debug":
            logger.setLevel(logging.DEBUG)
        elif loggerLevel == "info":
            logger.setLevel(logging.INFO)
        elif loggerLevel == "warning":
            logger.setLevel(logging.WARNING)
        elif loggerLevel == "error":
            logger.setLevel(logging.ERROR)
        elif loggerLevel == "critical":
            logger.setLevel(logging.CRITICAL)
            
        return logger

if __name__ == "__main__":
    
    '''
    Process of execution
    
    - Run the AWS import
    - Run the web Fetcher
    - Run the detector
    - Run AWS Export
    
    '''
   
    run = runner()
    
    parser = argparse.ArgumentParser(prog='Defacement Detection Engine',
                    description='Detects defaced websites')
    parser.add_argument('-l', '--logger', help="Choose the logger level (Overwrites the variable in the environment file)", required=False, )
    
    args = parser.parse_args()
    
    loggerLevel = args.logger
    loggerObj = run.generate_logger_file(loggerLevel)
    
    s3 = s3_interactions(loggerObj)
    sns = sns_interactions(loggerObj)
    detect = website_detection(loggerObj)
    fetch = website_fetcher(loggerObj)
    
    # Download the latest data
    s3.data_download()
    
    
    productionDirectoryWalk = fetch.dir_walker(PRODUCTION_WEBSITES_DOWNLOAD_LOCATION)
    fetch.web_fetcher(productionDirectoryWalk)
    liveDirectoryWalk = fetch.dir_walker(LIVE_WEBSITES_DOWNLOAD_LOCATION)
    
    ### Data cleaning ###
    for item in liveDirectoryWalk["domains"]:
        for key, value in item.items():
            for x in value:
                for nkey, nvalue in x.items():
                    try:
                        fetch.data_cleaning(fileName=f"{LIVE_WEBSITES_DOWNLOAD_LOCATION}/{nvalue}")
                    except UnicodeDecodeError as error:
                        print(f"Unicode Error - {error}")
    
    detect.comparison(productionDirectoryWalk, liveDirectoryWalk)
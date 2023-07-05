'''
Product: Environment File for WDDE
Description: Stores environment variables
Author: Benjamin Norman 2023
'''

### S3 CONFIG ###
BUCKET_NAME = "defacement-engine"

WEBSITES_LOCATION = "s3://defacement-engine/websites"

LOG_FILE_LOCATION = "logs/"

# Download location for within the Docker container

# No need for these to be modified
PRODUCTION_WEBSITES_DOWNLOAD_LOCATION = "./Data/Production_Data"

LIVE_WEBSITES_DOWNLOAD_LOCATION = "./Data/Live_Data"


### Logging ###

# DEBUG - Logs every stage of the process 
# INFO - Logs files that are not present in the production directory
# WARNING - Logs differences in files
# ERROR - Logs errors that can be accepted. e.g. missing files, non active websites, etc
# CRITICAL - Only logs events that would terminate the program, no website information is logged

# For all the necessary data to be logged, it is recommended that the logging level be set to INFO

LOGGING_LEVEL = "info"

### SNS CONFIG ###

NOTIFICATION_LIST = []
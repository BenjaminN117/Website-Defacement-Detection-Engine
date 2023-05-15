'''
Product: Environment File for WDDE
Description: Stores environment variables
Author: Benjamin Norman 2023
'''

### S3 CONFIG ###
BUCKET_NAME = "defacement-engine"

WEBSITES_LOCATION = "s3://defacement-engine/websites"

LOG_FILE_LOCATION = "S3://defacement-engine/logs/"

OUTPUT_FILE_LOCATION = "S3://defacement-engine/output/"


# Download location for within the Docker container

# That value is for testing only
PRODUCTION_WEBSITES_DOWNLOAD_LOCATION = "./"

LIVE_WEBSITES_DOWNLOAD_LOCATION = "./"



### SNS CONFIG ###

NOTIFICATION_LIST = []
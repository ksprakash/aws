import boto3
import logging
import subprocess
#from urllib.parse import quote,quote_plus

# Create a custom logger
logger = logging.getLogger('bucket_logging')

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('s3_bucket.txt')
logger.setLevel(logging.INFO)
logger.setLevel(logging.INFO)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

info = ['66747/Clients/829225/Client Information/Koenig Brothers Vitals 2021.xlsx']

#Declare needed 
s3 = boto3.client('s3')
source_bucket = 'cloudcabinet-backup-pre-purge-02-17-2021-oregon-region'
destination_bucket = 'CyberCabinet'



for key in info:
    key=key.lower()
    source_file = "{}/{}".format('prod',key)
    source = {'Bucket': source_bucket,'Key': source_file}
    print(source_file)
    print(source)
    
    try:
        logger.info(key)
        logger.info(s3.copy_object(CopySource=source,Bucket=destination_bucket,Key=key,ServerSideEncryption='AES256'))
        logger.info("================================================================================================")
        
    except Exception as err:
        logger.error(f'{err}- {key}')
        logger.error("================================================================================================")

# with open('D:\\Education\\git-operations\\s3_copy\\missing_files.txt','r') as missedfile:
#     data = missedfile.readlines()
#     for x in data:
#         info.append(x[13:].replace('\n',''))
# print(info)
# for x in info:
#     print(x)


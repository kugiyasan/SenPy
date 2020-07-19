import os
from dotenv import load_dotenv
# from boto.s3.connection import S3Connection

load_dotenv()

token = os.environ['token']
# token = S3Connection(os.environ['token'])
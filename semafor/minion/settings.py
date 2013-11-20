# Needed settings
S3_PATH = ''
AWS_KEY = ''
AWS_SECRET = ''
READABILITY_TOKEN = ''

# No need to change this settings
URLS_FILE = 'urls.input'
DATA_DIR = '/home/ubuntu/semafor/data'
SEMAFOR_DIR = '/home/ubuntu/semafor/semafor'

try:
    from local_settings import *
except:
    pass

import os
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

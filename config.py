
import os
from dotenv import load_dotenv

load_dotenv()

# YouTube Data API v3 configuration
API_KEY = os.getenv('YOUTUBE_API_KEY', 'YOUR_API_KEY_HERE')
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# Search parameters
COUNTRY_CODE = 'US'  
MAX_RESULTS = 50
CATEGORY_ID = None  

# Data storage paths
RAW_DATA_PATH = 'data/raw_data.json'
PROCESSED_DATA_PATH = 'data/processed_data.csv'
ANALYSIS_RESULTS_PATH = 'data/analysis_results.json'
VISUALIZATIONS_PATH = 'visualizations/'

# Analysis parameters
TOP_N_WORDS = 20
TOP_N_CHANNELS = 10
TOP_N_CATEGORIES = 10
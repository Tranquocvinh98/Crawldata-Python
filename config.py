import os
from dotenv import load_dotenv

load_dotenv()

dataset = ['analyst69', 'analyst11', 'analyst15', 'analyst39']
region=os.getenv('region')
universe=os.getenv('universe')
delay=os.getenv('delay')
path_token=os.getenv('path_token')
path_dataset=os.getenv('path_dataset')
api_dataset_information=os.getenv('api_dataset_information')
api_dataset=os.getenv('api_dataset')
alpha_count=os.getenv('alpha_count')
coverage=os.getenv('coverage')

POSTGRES_DB=os.getenv('POSTGRES_DB')
POSTGRES_USER=os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST=os.getenv('POSTGRES_HOST')
CONNECTION_STRING = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{5432}/{POSTGRES_DB}'



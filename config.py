# config.py
from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_KEY = getenv('API_KEY', None)
assert API_KEY

# use the key
print(API_KEY)
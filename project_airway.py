import requests
from bs4 import BeautifulSoup
import pandas as pd

url=f'https://www.airlinequality.com/airline-reviews/british-airways/'
html_content=requests.get(url)
html_content


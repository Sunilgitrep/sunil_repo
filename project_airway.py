import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

list_of_review=[]
url=f'https://www.airlinequality.com/airline-reviews/british-airways/'
html_content=requests.get(url).content
soup=BeautifulSoup(html_content,'lxml')
articles=soup.find_all('article',attrs={'itemprop':'review'})

for article in articles:
    recorded_date=str(datetime.date.today())
    title=article.find('h2',attrs={'class':'text_header'}).get_text()
    review_date=article.find('time',attrs={'itemprop':'datePublished'})['datetime']
    country=article.find('h3',attrs={'class':'text_sub_header userStatusWrapper'}).get_text().split('(')[1].split(')')[0]
    review=article.find('div',attrs={'class':'text_content'}).get_text()
    rating=article.find('span',attrs={'itemprop':'ratingValue'}).get_text()

    dictionary_of_review={}
    dictionary_of_review['recorded_date']=recorded_date
    dictionary_of_review['title']=title
    dictionary_of_review['review_date']=review_date
    dictionary_of_review['country']=country
    dictionary_of_review['review']=review
    dictionary_of_review['rating']=rating
    list_of_review.append(dictionary_of_review)

pd.json_normalize(list_of_review)
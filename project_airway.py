import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from sqlalchemy import create_engine,MetaData,Table,Integer,String,Text,Column

server = 'airlineserver14.database.windows.net'
database = 'airlinedatabase'
username = 'airlineadmin'
password = 'Airline@14'
driver = '{ODBC Driver 17 for SQL Server}'

connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

con = create_engine(f"mssql+pyodbc:///?odbc_connect={connection_string}")



i=1
while(True):
    list_of_review=[]
    url=f'https://www.airlinequality.com/airline-reviews/british-airways/page/{i}/'
    html_content=requests.get(url).content
    soup=BeautifulSoup(html_content,'lxml')
    articles=soup.find_all('article',attrs={'itemprop':'review'})
    if (articles==[]):
        break

    for article in articles:
        recorded_date=str(datetime.date.today())
        title=article.find('h2',attrs={'class':'text_header'}).get_text()
        review_date=article.find('time',attrs={'itemprop':'datePublished'})['datetime']
        country=article.find('h3',attrs={'class':'text_sub_header userStatusWrapper'}).get_text().split('(')[1].split(')')[0]
        review=article.find('div',attrs={'class':'text_content'}).get_text()
        rating=article.find('span',attrs={'itemprop':'ratingValue'}).get_text()
        table=article.find('table',attrs={'class':'review-ratings'})
        table_rows=table.find_all('tr')
        d={}
        for table_row in table_rows:
            table_data=table_row.find_all('td')
            key=table_data[0].get_text()
            value=table_data[1]
            if(value['class']==['review-rating-stars', 'stars']):
                value=len(value.find_all('span',attrs={'class':'star fill'}))
            else:
                value=value.get_text()

            d[key]=value

        dictionary_of_review={}
        dictionary_of_review['recorded_date']=recorded_date
        dictionary_of_review['title']=title
        dictionary_of_review['review_date']=review_date
        dictionary_of_review['country']=country
        dictionary_of_review['review']=review
        dictionary_of_review['rating']=rating
        dictionary_of_review['details']=d
        list_of_review.append(dictionary_of_review)
    print (f'collecting data from page {i}')
    df=pd.json_normalize(list_of_review)
    df.columns = df.columns.str.replace('details.','').str.replace(' & ','_').str.replace(' ','_').str.lower()

    # dataframe to sql
    df.to_sql(name='airlinetable',con=con,schema='dbo',index=False,if_exists='append')
    
    i=i+1

df.to_csv('british_a.csv',index=False)
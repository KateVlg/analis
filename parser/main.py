# scraper.py
import requests
from bs4 import BeautifulSoup
import traceback
from pymongo import MongoClient
import uuid

myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["vlg_news"]
mycol = mydb["news_docs"]

def resp(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'lxml')


def parsobj(tg, cls):
    quotes = soup.find_all(tg, class_=cls)
    return quotes[0].contents[0]

html_doc = """vlg-media.ru"""
soup = BeautifulSoup(html_doc, 'html.parser')
quotes = soup.find_all('div', class_='uk-card-title')

for div in quotes:
    try:
        if div.name:
            lnk = div.find('a')
            url = lnk.get('href')
            soup = resp(url)

            name_news = parsobj('h1', 'entry-title')
            num_comments = parsobj('span', 'wpdtc')
            quotes = soup.find_all('header', class_='entry-header')
            for header in quotes:
                if header.name:
                    dt = header.find('time')
                    date_news = dt.contents[0]

            text_news = ''
            quotes = soup.find_all('div', class_='entry-content')
            for div in quotes:
                if div.name:
                    tx = div.find_all('p')
                    for i in range(1, tx.__len__()):
                        for y in range(tx[i].contents.__len__()):
                            obj = str(tx[i].contents[y])
                            if 'href' in obj:
                                obj = str(tx[i].contents[y].contents[0])
                            else:
                                obj = str(tx[i].contents[y])

                            if ('<strong>' in obj) and ('</strong>' in obj):
                                obj = obj.replace('<strong>', '')
                                obj = obj.replace('</strong>', '')
                            if not('<br/>' in obj):
                                text_news += obj

            tmpid = (str(uuid.uuid4().hex))[0:24]
            line = {'_id': {'oid': tmpid}, 'name_news': name_news, 'date_news': date_news, 'link_news': url,
                    'text_news': text_news, 'num_comments': num_comments}
            x = mycol.insert_one(line)

    except Exception as e:
        print('Ошибка:\n', traceback.format_exc())


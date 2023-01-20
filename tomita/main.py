from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson import ObjectId
import os.path

# Подключение к MongoDB
myclient = MongoClient("mongodb://localhost:27017/")
mydb = myclient["vlg_news"]
mycol = mydb["news_docs"]

i = 0

# Цикл, который обходит все статьи в коллекции
for articles in mycol.find():
    i += 1
    print(i)

    os.chdir('/home/student/tomita-parser/build/bin')
    # запуск томита-парсера
    os.system('./tomita-parser config.proto')
    os.chdir('/home/student/PycharmProjects/SemesterKompLing/second')

    # получаем предложения
    sentens = ""
    f = open("/home/student/tomita-parser/build/bin/output.html", "r")
    contents = f.read()
    soup = BeautifulSoup(contents, 'html.parser')
    for tag in soup.find('table').findAll('a'):
        sentens += str("{1}".format(tag.name, tag.text) + " ")

    f.close()

    sentens = sentens.replace("'", "")
    sentens = sentens.replace(" .,", ".")

    ID = articles.get("_id")

    mycol.find_one_and_update({'_id': ObjectId(ID)}, {"$set": {'sentens': sentens}})
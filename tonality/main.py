# -*- coding: utf-8 -*-
import numpy as np
import csv
import re
import sys
import fasttext

from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)

lst = [] # массив всех данных (сюда заносятся всё, с готовым анализом)

#fasttext.FastText.eprint = lambda x: None
# открытие csv файла
with open("news_docs (2).csv", "r", encoding='utf-8') as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if line[5] != (""):
            messages = line[5]
            results = model.predict(messages, k=5)
            sentiment = results[0]
            #print(sentiment)
            positive = round(sentiment["positive"], 5)
            negative = round(sentiment["negative"], 5)
            neutral = round(sentiment["neutral"], 5)
            speech = round(sentiment["speech"], 5)
            skip = round(sentiment["skip"], 5)
            m = max(positive, negative, neutral, speech, skip)
            if positive < negative:
                line.append("Негативное")
            else:
                line.append("Позитивное")
        else:
            line.append("Аргументы не предоставлены")
        lst.append(line)

with open("output.txt", "w", encoding='utf-8') as f:
    for i in lst:
        k = "^".join([str(x) for x in i])+"\n"
        f.write(k)




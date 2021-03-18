import requests
import pandas as pd
from bs4 import BeautifulSoup

urls = ['https://ourage.jp/column/karada_genki/','https://ourage.jp/column/otona_beauty/',
       'https://ourage.jp/column/kounenki_no_chie/','https://ourage.jp/column/life/',
      'https://ourage.jp/column/odekake_joshigumi/','https://ourage.jp/column/food/',
      'https://ourage.jp/column/future_planning/']

def get_articles(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find(name="h1", class_="article__title").text
    content = soup.find(name="div", class_="article__content").text
    title_and_content = title + ' ' + content
    return title, content, title_and_content

def get_trend_contents(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    results = soup.find_all(name="div", class_="rankings js_ranking-list-numbering")
    article_list = []
    for result in results:
        atags = result.find_all("a")
        for atag in atags:
            article_url = atag.get("href")
            title, content, title_and_content = get_articles(article_url)
            article_list.append((article_url, title, content, title_and_content))
    return article_list

writer = pd.ExcelWriter('article_data.xlsx', engine='xlsxwriter')
for category_url in urls:
    category = category_url.replace('https://ourage.jp/column/','').replace('/','')
    article_list = get_trend_contents(category_url)
    df = pd.DataFrame(article_list, columns =['url', 'title', 'content', 'title_and_content'])
    df.to_excel(writer, sheet_name=category)
writer.save()
    

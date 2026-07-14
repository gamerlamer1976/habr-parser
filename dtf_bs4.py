

import bs4
import requests
import json

response = requests.get('https://dtf.ru/games')
soup = bs4.BeautifulSoup(response.text, features='lxml')

articles_block = soup.select_one('div.content-list')
articles_list = articles_block.select('div.content.content--short')


data = []
for article in articles_list:
    link_div = article.select_one('div.content-title')
    link = 'https://dtf.ru' + link_div.select_one('a')['href']

    response = requests.get(link)
    article_soup = bs4.BeautifulSoup(response.text, features='lxml')

    title = article_soup.select_one('h1').text.strip()
    time = article_soup.select_one('time')['title']
    text = article_soup.select_one('article.content__blocks').text.strip()

    data.append({
        'link': link,
        'title': title,
        'time': time,
        'text': text,
    })

with open('articles.json', 'w') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

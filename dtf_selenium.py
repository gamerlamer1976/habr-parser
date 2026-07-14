import json
from time import sleep

from selenium.webdriver import Chrome, ChromeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from dtf_bs4 import title

# response = requests.get('https://dtf.ru/games')
# soup = bs4.BeautifulSoup(response.text, features='lxml')

driver = Chrome()
driver.get('https://dtf.ru/games')
sleep(5)


# # articles_block = soup.select_one('div.content-list')
# # articles_list = articles_block.select('div.content.content--short')
#
# articles_block = driver.find_element(By.CSS_SELECTOR, 'div.content-list')
# articles_list = articles_block.find_elements(By.CSS_SELECTOR, 'div.content.content--short')
#
# data = []
# links = []
# for article in articles_list:
# #     link_div = article.select_one('div.content-title')
# #     link = 'https://dtf.ru' + link_div.select_one('a')['href']
#     link_div = article.find_element(By.CSS_SELECTOR, 'div.content-title')
#     link = link_div.find_element(By.TAG_NAME, 'a').get_attribute('href')
#     links.append(link)
#
# #     response = requests.get(link)
# #     article_soup = bs4.BeautifulSoup(response.text, features='lxml')
#
# for link in links:
#     driver.get(link)
#     sleep(1)
#
#
# #     title = article_soup.select_one('h1').text.strip()
#     title = driver.find_element(By.TAG_NAME, 'h1').text.strip()
# #     time = article_soup.select_one('time')['title']
#     time = driver.find_element(By.TAG_NAME, 'time').get_attribute('title')
# #     text = article_soup.select_one('article.content__blocks').text.strip()
#     text = driver.find_element(By.CSS_SELECTOR, 'article.content__blocks').text.strip()
#
#     data.append({
#         'link': link,
#         'title': title,
#         'time': time,
#         'text': text,
#     })
#
# with open('articles2.json', 'w') as file:
#     json.dump(data, file, ensure_ascii=False, indent=2)


# search_button = driver.find_element(By.CSS_SELECTOR, 'button.quick-search-button')
# search_button.click()
# sleep(5)
#
# search_field = driver.find_element(By.CSS_SELECTOR, 'input.text-input')
# sleep(5)
# search_field.send_keys('fallout')
# sleep(5)
# search_field.send_keys(Keys.ENTER)
# sleep(10)
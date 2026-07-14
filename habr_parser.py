import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

# 1. Генерируем заголовки
headers = Headers(browser="chrome", os="win").generate()
URL = 'https://habr.com/ru/articles/'

# 2. Запрос
response = requests.get(URL, headers=headers)
print("Статус:", response.status_code)

# 3. Парсинг
soup = BeautifulSoup(response.text, 'html.parser')
articles = soup.find_all('article', class_='tm-articles-list__item')

# 4. Обработка
for article in articles:
    h2_tag = article.find('h2')
    time_tag = article.find('time')

    # Находим ссылку
    link_tag = h2_tag.find('a') if h2_tag else None

    # Проверка существования элементов
    if link_tag and time_tag:
        # Извлекаем href (get возвращает None, если атрибута нет)
        href = link_tag.get('href')

        # Если href — строка, работаем дальше
        if isinstance(href, str):
            title = link_tag.get_text(strip=True)
            date = time_tag.get('title', 'Дата не указана')
            link = "https://habr.com" + href

            # Вывод результата
            print(f"Дата: {date}")
            print(f"Заголовок: {title}")
            print(f"Ссылка: {link}")
            print("-" * 30)

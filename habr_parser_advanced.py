import time
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

# Список ключевых слов:
KEYWORDS = ['дизайна', 'фото', 'web', 'python']


def get_full_text(link: str, headers: dict) -> str:
    """Функция для перехода внутрь статьи."""
    try:
        response = requests.get(link, headers=headers, timeout=10)
        # Проверяем, что ответ успешный
        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find('div', class_='tm-article-body')

        # Безопасно получаем текст
        if body:
            return str(body.get_text(strip=True).lower())
        return ""
    except Exception:
        return ""


def main():
    headers = Headers(browser="chrome", os="win").generate()
    url = 'https://habr.com/ru/articles/'

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='tm-articles-list__item')

    for article in articles:
        h2_tag = article.find('h2')
        # Всегда проверяем наличие тега перед поиском внутри него
        if h2_tag:
            link_tag = h2_tag.find('a')
            # Безопасное получение href через .get()
            href = link_tag.get('href') if link_tag else None

            if href and isinstance(href, str):
                title = str(h2_tag.get_text(strip=True))
                full_link = "https://habr.com" + href

                # Анализируем полный текст
                full_text = get_full_text(full_link, headers)

                # Проверка вхождения слов
                if any(word.lower() in full_text for word in KEYWORDS):
                    time_tag = article.find('time')
                    date = str(time_tag.get('title', 'Дата не указана')) if time_tag else 'Дата не указана'
                    print(f"{date} – {title} – {full_link}")

                time.sleep(1)


if __name__ == '__main__':
    main()

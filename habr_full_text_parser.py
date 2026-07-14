import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import time
import json
from typing import Optional, List, Dict, Any

# ============================================================================
# 1. НАСТРОЙКИ
# ============================================================================
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/articles/'
MAX_ARTICLES_TO_CHECK = 5  # Ограничим количество для теста

# Генерируем заголовки браузера
headers = Headers(browser='chrome', os='win').generate()

print(f"📥 Шаг 1: Получаем список свежих статей с {URL}...")
response = requests.get(URL, headers=headers)

if response.status_code != 200:
    print(f"❌ Ошибка доступа к сайту. Код: {response.status_code}")
    exit(1)

soup = BeautifulSoup(response.text, 'html.parser')
articles = soup.find_all('article', class_='tm-articles-list__item')[:MAX_ARTICLES_TO_CHECK]

print(f"✅ Найдено статей для глубокого анализа: {len(articles)}")
print("=" * 80)


# ============================================================================
# 2. ФУНКЦИЯ ДЛЯ ПОЛУЧЕНИЯ ПОЛНОГО ТЕКСТА СТАТЬИ
# ============================================================================
def get_full_article_text(article_url: str) -> Optional[str]:
    """
    Переходит по ссылке статьи и возвращает полный текст.
    """
    full_url = "https://habr.com" + article_url if not article_url.startswith('http') else article_url

    try:
        full_response = requests.get(full_url, headers=headers, timeout=10)

        if full_response.status_code != 200:
            return None

        article_soup = BeautifulSoup(full_response.text, 'html.parser')

        # На Хабр основной текст статьи лежит в div с классом tm-article-body
        content_div = article_soup.find('div', class_='tm-article-body')

        if not content_div:
            content_div = article_soup.find('article')

        if content_div:
            full_text = content_div.get_text(' ', strip=True)
            # Явно преобразуем к строке и нижнему регистру
            return str(full_text).lower()
        else:
            return None

    except Exception as e:
        print(f"   ❌ Ошибка при загрузке {full_url}: {e}")
        return None


# ============================================================================
# 3. ОБРАБОТКА КАЖДОЙ СТАТЬИ
# ============================================================================
matched_articles: List[Dict[str, Any]] = []

for idx, article in enumerate(articles, 1):
    print(f"\n[{idx}/{len(articles)}] Анализируем статью...")

    # --- Извлекаем базовую информацию ---
    time_tag = article.find('time')
    if time_tag:
        date_attr = time_tag.get('title') or time_tag.get('datetime')
        if date_attr and isinstance(date_attr, str):
            date = date_attr.split('T')[0] if 'T' in date_attr else date_attr
        else:
            date = "Дата не указана"
    else:
        date = "Дата не указана"

    h2_tag = article.find('h2', class_='tm-title')
    if h2_tag:
        link_tag = h2_tag.find('a')
        if link_tag:
            title = link_tag.get_text(strip=True)
            href = link_tag.get('href')
            if href and isinstance(href, str):
                link = "https://habr.com" + href
            else:
                link = "Нет ссылки"
                href = None
        else:
            title = "Без заголовка"
            link = "Нет ссылки"
            href = None
    else:
        title = "Без заголовка"
        link = "Нет ссылки"
        href = None

    if not href:
        print("   ⚠️ Нет ссылки, пропускаем.")
        continue

    # --- Получаем ПОЛНЫЙ текст статьи ---
    print(f"   ⏳ Загружаем полный текст: {href}")
    article_full_text = get_full_article_text(href)

    if not article_full_text:
        print("   ⚠️ Не удалось извлечь текст статьи.")
        time.sleep(2)
        continue

    # --- Ищем ключевые слова в ПОЛНОМ тексте ---
    found_keywords: List[str] = []
    keyword_counts: Dict[str, int] = {}

    for keyword in KEYWORDS:
        if keyword.lower() in article_full_text:
            found_keywords.append(keyword)
            keyword_counts[keyword] = article_full_text.count(keyword.lower())

    # --- Формируем результат ---
    if found_keywords:
        print(f"   ✅ СОВПАДЕНИЕ в полном тексте!")
        print(f"   📅 {date} – {title}")
        print(f"   🔑 Найдены слова: {', '.join([f'{k} ({v} раз)' for k, v in keyword_counts.items()])}")

        matched_articles.append({
            'date': date,
            'title': title,
            'link': link,
            'found_keywords': found_keywords,
            'keyword_counts': keyword_counts
        })
    else:
        print(f"   ❌ Ключевые слова в полном тексте не найдены.")

    # ⚠️ ВАЖНО: Делаем паузу
    time.sleep(2)

# ============================================================================
# 4. СОХРАНЕНИЕ РЕЗУЛЬТАТОВ В JSON
# ============================================================================
print("\n" + "=" * 80)
print(f"💾 Сохраняем результаты в файл 'habr_full_results.json'...")

with open('habr_full_results.json', 'w', encoding='utf-8') as file:
    json.dump(matched_articles, file, ensure_ascii=False, indent=4)

print(f"✅ ГОТОВО! Найдено {len(matched_articles)} статей из {len(articles)} проверенных.")
print("📂 Данные сохранены в habr_full_results.json")

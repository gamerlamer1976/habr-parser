import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from typing import List, Dict, Optional

# ============================================================================
# 1. ОПРЕДЕЛЯЕМ КЛЮЧЕВЫЕ СЛОВА ДЛЯ ПОИСКА
# ============================================================================
KEYWORDS: List[str] = ['дизайн', 'фото', 'web', 'python']

# ============================================================================
# 2. НАСТРАИВАЕМ ЗАПРОС
# ============================================================================
URL: str = 'https://habr.com/ru/articles/'

headers: Dict[str, str] = Headers(browser='chrome', os='win').generate()

print(f"Подключаемся к {URL}...")
response = requests.get(URL, headers=headers)

if response.status_code != 200:
    print(f"❌ Ошибка доступа к сайту. Код: {response.status_code}")
    exit(1)

print(f"✅ Успешно получили страницу (статус {response.status_code})")

# ============================================================================
# 3. ПАРСИМ HTML
# ============================================================================
soup = BeautifulSoup(response.text, 'html.parser')
articles = soup.find_all('article', class_='tm-articles-list__item')

print(f"Найдено статей на странице: {len(articles)}")
print(f"Ищем ключевые слова: {', '.join(KEYWORDS)}")
print("=" * 80)


# ============================================================================
# 4. ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ: безопасное извлечение текста
# ============================================================================
def safe_text(element: Optional[object]) -> str:
    """Безопасно получает текст из элемента, возвращает пустую строку если None."""
    if element is None:
        return ""
    if hasattr(element, 'get_text'):
        text = element.get_text(' ', strip=True)
        return str(text) if text else ""
    return ""


# ============================================================================
# 5. ОБРАБАТЫВАЕМ КАЖДУЮ СТАТЬЮ
# ============================================================================
matched_articles: List[Dict[str, str]] = []

for idx, article in enumerate(articles, 1):
    # --- 5.1. ИЗВЛЕКАЕМ ЗАГОЛОВОК (теперь участвует в поиске!) ---
    h2_tag = article.find('h2', class_='tm-title')
    title: str = ""
    href: Optional[str] = None
    link: str = "Ссылка недоступна"

    if h2_tag:
        link_tag = h2_tag.find('a')
        if link_tag:
            title = str(link_tag.get_text(strip=True))
            href_raw = link_tag.get('href')
            if href_raw and isinstance(href_raw, str):
                href = href_raw
                link = "https://habr.com" + href_raw

    # --- 5.2. ИЗВЛЕКАЕМ ДАТУ ---
    time_tag = article.find('time')
    date: str = "Дата не указана"
    if time_tag:
        date_attr = time_tag.get('title') or time_tag.get('datetime')
        if date_attr and isinstance(date_attr, str):
            date = date_attr.split('T')[0] if 'T' in date_attr else date_attr
        else:
            date_text = time_tag.get_text(strip=True)
            if isinstance(date_text, str) and date_text:
                date = date_text

    # --- 5.3. ИЗВЛЕКАЕМ ТЕКСТ ПРЕВЬЮ (анонс) ---
    preview_div = article.find('div', class_='tm-article-snippet__lead')
    preview_text: str = safe_text(preview_div)

    # --- 5.4. ИЗВЛЕКАЕМ ТЕГИ ---
    tags_block = article.find('div', class_='tm-article-snippet__tags')
    tags_text: str = safe_text(tags_block)

    # --- 5.5. ИЗВЛЕКАЕМ АВТОРА ---
    author_link = article.find('a', class_='tm-user-info__user')
    author_text: str = safe_text(author_link)

    # --- 5.6. ИЗВЛЕКАЕМ ХАБ/КАТЕГОРИЮ ---
    hub_link = article.find('a', class_='tm-article-hub__link')
    hub_text: str = safe_text(hub_link)

    # --- 5.7. ФОРМИРУЕМ ПОЛНЫЙ ТЕКСТ ДЛЯ ПОИСКА ---
    # ВАЖНО: объединяем ВСЕ видимые текстовые элементы превью
    search_text: str = " ".join([
        title,
        preview_text,
        tags_text,
        author_text,
        hub_text
    ]).lower()

    # --- 5.8. ИЩЕМ КЛЮЧЕВЫЕ СЛОВА ---
    found_keywords: List[str] = []
    for keyword in KEYWORDS:
        if keyword.lower() in search_text:
            found_keywords.append(keyword)

    # --- 5.9. ЕСЛИ НАЙДЕНЫ СОВПАДЕНИЯ ---
    if found_keywords:
        matched_articles.append({
            'date': date,
            'title': title,
            'link': link,
            'keywords': ', '.join(found_keywords)
        })

        # Вывод в требуемом формате: <дата> – <заголовок> – <ссылка>
        print(f"{date} – {title} – {link}")
        print(f"   🔑 Найдены слова: {', '.join(found_keywords)}")
        print(f"   📝 Поиск велся в: заголовок, анонс, теги, автор, хаб")
        print("-" * 80)

# ============================================================================
# 6. ИТОГОВАЯ СТАТИСТИКА
# ============================================================================
print("\n" + "=" * 80)
print(f"✅ ВСЕГО НАЙДЕНО СТАТЕЙ: {len(matched_articles)} из {len(articles)}")
if articles:
    percentage: float = len(matched_articles) / len(articles) * 100
    print(f"📊 Процент совпадений: {percentage:.1f}%")

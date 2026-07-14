import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

# ============================================================================
# 1. ОПРЕДЕЛЯЕМ КЛЮЧЕВЫЕ СЛОВА ДЛЯ ПОИСКА
# ============================================================================
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

# ============================================================================
# 2. НАСТРАИВАЕМ ЗАПРОС
# ============================================================================
URL = 'https://habr.com/ru/articles/'

# Генерируем заголовки браузера
headers = Headers(browser='chrome', os='win').generate()

# Делаем запрос к странице
print(f"Подключаемся к {URL}...")
response = requests.get(URL, headers=headers)

# Проверяем успешность запроса
if response.status_code != 200:
    print(f"❌ Ошибка доступа к сайту. Код: {response.status_code}")
    exit(1)

print(f"✅ Успешно получили страницу (статус {response.status_code})")

# ============================================================================
# 3. ПАРСИМ HTML
# ============================================================================
soup = BeautifulSoup(response.text, 'html.parser')

# Находим все статьи на странице
articles = soup.find_all('article', class_='tm-articles-list__item')

print(f" Найдено статей на странице: {len(articles)}")
print(f" Ищем ключевые слова: {', '.join(KEYWORDS)}")
print("=" * 80)

# ============================================================================
# 4. ОБРАБАТЫВАЕМ КАЖДУЮ СТАТЬЮ
# ============================================================================
matched_articles = []

for idx, article in enumerate(articles, 1):
    # --- ИЗВЛЕКАЕМ ДАТУ ---
    time_tag = article.find('time')
    if time_tag:
        # Получаем дату из атрибута datetime
        date_attr = time_tag.get('datetime')
        if date_attr and isinstance(date_attr, str):
            # Убираем время, если есть (разделяем по 'T')
            date = date_attr.split('T')[0]
        else:
            # Если нет datetime, берем текст
            date_text = time_tag.get_text(strip=True)
            date = date_text if isinstance(date_text, str) else "Дата не указана"
    else:
        date = "Дата не указана"

    # --- ИЗВЛЕКАЕМ ЗАГОЛОВОК И ССЫЛКУ ---
    h2_tag = article.find('h2', class_='tm-title')
    if h2_tag:
        link_tag = h2_tag.find('a')
        if link_tag:
            title = link_tag.get_text(strip=True)
            href = link_tag.get('href')
            # Формируем полную ссылку
            if href and isinstance(href, str):
                link = "https://habr.com" + href
            else:
                link = "Ссылка недоступна"
        else:
            title = "Заголовок не найден"
            link = "Ссылка недоступна"
    else:
        title = "Заголовок не найден"
        link = "Ссылка недоступна"

    # --- ИЗВЛЕКАЕМ ТЕКСТ ПРЕВЬЮ ---
    preview_div = article.find('div', class_='article-formatted-body')
    if not preview_div:
        preview_div = article.find('div', class_='tm-article-body')

    if preview_div:
        preview_text = preview_div.get_text(' ', strip=True)
        # Преобразуем в строку и к нижнему регистру
        if isinstance(preview_text, str):
            preview_text = preview_text.lower()
        else:
            preview_text = ""
    else:
        preview_text = ""

    # --- ИЩЕМ КЛЮЧЕВЫЕ СЛОВА ---
    found_keywords = []
    for keyword in KEYWORDS:
        if keyword.lower() in preview_text:
            found_keywords.append(keyword)

    # --- ЕСЛИ НАЙДЕНЫ СОВПАДЕНИЯ ---
    if found_keywords:
        matched_articles.append({
            'date': date,
            'title': title,
            'link': link,
            'keywords': found_keywords
        })

        # Выводим результат в требуемом формате
        print(f"{date} – {title} – {link}")
        print(f"   🔑 Найдены слова: {', '.join(found_keywords)}")
        print("-" * 80)

# ============================================================================
# 5. ИТОГОВАЯ СТАТИСТИКА
# ============================================================================
print("\n" + "=" * 80)
print(f"✅ ВСЕГО НАЙДЕНО СТАТЕЙ: {len(matched_articles)} из {len(articles)}")
if articles:
    percentage = len(matched_articles) / len(articles) * 100
    print(f"📊 Процент совпадений: {percentage:.1f}%")

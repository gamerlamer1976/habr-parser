import requests
from bs4 import BeautifulSoup, Tag
from fake_headers import Headers
import time
import json
from typing import List, Dict, Optional, Union

# ============================================================================
# 1. НАСТРОЙКИ
# ============================================================================
KEYWORDS: List[str] = ['дизайн', 'фото', 'web', 'python']
URL: str = 'https://habr.com/ru/articles/'
MAX_ARTICLES: int = 10

headers: Dict[str, str] = Headers(browser='chrome', os='win').generate()


# ============================================================================
# 2. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================================
def safe_text(element: Optional[Union[Tag, object]]) -> str:
    """Безопасно получает текст из элемента."""
    if element is None:
        return ""
    if hasattr(element, 'get_text'):
        text = element.get_text(' ', strip=True)
        return str(text) if text else ""
    return ""


def get_full_article_text(article_url: str) -> Optional[str]:
    """Загружает полный текст статьи по ссылке."""
    full_url: str = "https://habr.com" + article_url if not article_url.startswith('http') else article_url

    try:
        full_response = requests.get(full_url, headers=headers, timeout=10)

        if full_response.status_code != 200:
            return None

        article_soup: BeautifulSoup = BeautifulSoup(full_response.text, 'html.parser')
        content_div: Optional[Tag] = article_soup.find('div', class_='tm-article-body')

        if not content_div:
            content_div = article_soup.find('article')

        if content_div:
            full_text: str = content_div.get_text(' ', strip=True)
            return str(full_text).lower()
        else:
            return None

    except Exception as e:
        print(f"   ❌ Ошибка при загрузке {full_url}: {e}")
        return None


def extract_preview_search_text(article_element: Tag) -> str:
    """Извлекает ВСЕ текстовые поля превью для поиска."""
    # Заголовок
    h2_tag: Optional[Tag] = article_element.find('h2', class_='tm-title')
    title_text: str = ""
    if h2_tag:
        link_tag: Optional[Tag] = h2_tag.find('a')
        if link_tag:
            title_text = str(link_tag.get_text(strip=True))

    # Анонс
    preview_div: Optional[Tag] = article_element.find('div', class_='tm-article-snippet__lead')
    preview_text: str = safe_text(preview_div)

    # Теги
    tags_block: Optional[Tag] = article_element.find('div', class_='tm-article-snippet__tags')
    tags_text: str = safe_text(tags_block)

    # Автор
    author_link: Optional[Tag] = article_element.find('a', class_='tm-user-info__user')
    author_text: str = safe_text(author_link)

    # Хаб/категория
    hub_link: Optional[Tag] = article_element.find('a', class_='tm-article-hub__link')
    hub_text: str = safe_text(hub_link)

    # Объединяем всё
    return " ".join([title_text, preview_text, tags_text, author_text, hub_text]).lower()


def extract_article_info(article_element: Tag) -> Dict[str, str]:
    """Извлекает базовую информацию о статье."""
    info_dict: Dict[str, str] = {
        'date': 'Дата не указана',
        'title': 'Без заголовка',
        'link': 'Нет ссылки',
        'href': ''
    }

    # Дата
    time_tag: Optional[Tag] = article_element.find('time')
    if time_tag:
        # Исправление: явно преобразуем к str
        date_attr_raw = time_tag.get('title') or time_tag.get('datetime')
        date_attr: Optional[str] = str(date_attr_raw) if date_attr_raw else None

        if date_attr and isinstance(date_attr, str):
            info_dict['date'] = date_attr.split('T')[0] if 'T' in date_attr else date_attr
        else:
            date_text: str = time_tag.get_text(strip=True)
            if isinstance(date_text, str) and date_text:
                info_dict['date'] = date_text

    # Заголовок и ссылка
    h2_tag: Optional[Tag] = article_element.find('h2', class_='tm-title')
    if h2_tag:
        link_tag: Optional[Tag] = h2_tag.find('a')
        if link_tag:
            info_dict['title'] = str(link_tag.get_text(strip=True))
            # Исправление: явно преобразуем href к str
            href_raw = link_tag.get('href')
            href: Optional[str] = str(href_raw) if href_raw else None

            if href and isinstance(href, str):
                info_dict['href'] = href
                info_dict['link'] = "https://habr.com" + href

    return info_dict


# ============================================================================
# 3. ПОЛУЧАЕМ СПИСОК СТАТЕЙ
# ============================================================================
print(f"📥 Шаг 1: Получаем список свежих статей с {URL}...")
response = requests.get(URL, headers=headers)

if response.status_code != 200:
    print(f"❌ Ошибка доступа к сайту. Код: {response.status_code}")
    exit(1)

soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
articles_list: List[Tag] = soup.find_all('article', class_='tm-articles-list__item')[:MAX_ARTICLES]

print(f"✅ Найдено статей для анализа: {len(articles_list)}")
print(f"🔑 Ключевые слова: {', '.join(KEYWORDS)}")
print("=" * 80)

# ============================================================================
# 4. ОБРАБОТКА КАЖДОЙ СТАТЬИ
# ============================================================================
matched_articles: List[Dict[str, object]] = []
preview_found_count: int = 0
full_text_found_count: int = 0

for article_idx, article_elem in enumerate(articles_list, 1):
    print(f"\n[{article_idx}/{len(articles_list)}] Анализируем статью...")

    # --- 4.1. Извлекаем базовую информацию ---
    article_info: Dict[str, str] = extract_article_info(article_elem)
    article_date: str = article_info['date']
    article_title: str = article_info['title']
    article_link: str = article_info['link']
    article_href: str = article_info['href']

    if not article_href:
        print("   ⚠️ Нет ссылки, пропускаем.")
        continue

    # --- 4.2. ЭТАП 1: Ищем в ПРЕВЬЮ (быстро, без загрузки страницы) ---
    print(f"   🔍 Этап 1: Поиск в превью...")
    preview_search_text: str = extract_preview_search_text(article_elem)

    preview_keywords: List[str] = []
    for keyword in KEYWORDS:
        if keyword.lower() in preview_search_text:
            preview_keywords.append(keyword)

    if preview_keywords:
        # ✅ НАШЛИ В ПРЕВЬЮ — полный текст загружать НЕ нужно!
        preview_found_count += 1
        print(f"   ✅ НАЙДЕНО В ПРЕВЬЮ!")
        print(f"   📅 {article_date} – {article_title}")
        print(f"   🔑 Слова: {', '.join(preview_keywords)}")

        matched_articles.append({
            'date': article_date,
            'title': article_title,
            'link': article_link,
            'source': 'preview',
            'found_keywords': preview_keywords,
            'keyword_counts': {k: preview_search_text.count(k.lower()) for k in preview_keywords}
        })
        continue  # Переходим к следующей статье, полный текст не грузим!

    # --- 4.3. ЭТАП 2: Не нашли в превью — загружаем ПОЛНЫЙ ТЕКСТ ---
    print(f"    Этап 2: В превью не найдено. Загружаем полный текст...")
    article_full_text: Optional[str] = get_full_article_text(article_href)

    if not article_full_text:
        print("    Не удалось загрузить полный текст.")
        time.sleep(2)
        continue

    # Ищем в полном тексте
    full_keywords: List[str] = []
    for keyword in KEYWORDS:
        if keyword.lower() in article_full_text:
            full_keywords.append(keyword)

    if full_keywords:
        # ✅ НАШЛИ В ПОЛНОМ ТЕКСТЕ
        full_text_found_count += 1
        keyword_counts_dict: Dict[str, int] = {k: article_full_text.count(k.lower()) for k in full_keywords}

        print(f"   ✅ НАЙДЕНО В ПОЛНОМ ТЕКСТЕ!")
        print(f"   📅 {article_date} – {article_title}")
        print(f"   🔑 Слова: {', '.join([f'{k} ({v} раз)' for k, v in keyword_counts_dict.items()])}")

        matched_articles.append({
            'date': article_date,
            'title': article_title,
            'link': article_link,
            'source': 'full_text',
            'found_keywords': full_keywords,
            'keyword_counts': keyword_counts_dict
        })
    else:
        print(f"   ❌ Ключевые слова не найдены ни в превью, ни в полном тексте.")

    # Пауза между запросами (только если загружали полный текст)
    time.sleep(2)

# ============================================================================
# 5. СОХРАНЕНИЕ РЕЗУЛЬТАТОВ В JSON
# ============================================================================
print("\n" + "=" * 80)
print("📊 ИТОГОВАЯ СТАТИСТИКА")
print(f"   Найдено в превью: {preview_found_count}")
print(f"   Найдено в полном тексте: {full_text_found_count}")
print(f"   Всего найдено: {len(matched_articles)} из {len(articles_list)}")

print(f"\n💾 Сохраняем результаты в файл 'habr_full_results.json'...")

with open('habr_full_results.json', 'w', encoding='utf-8') as file:
    json.dump(matched_articles, file, ensure_ascii=False, indent=4)

print(f"✅ ГОТОВО! Данные сохранены в habr_full_results.json")

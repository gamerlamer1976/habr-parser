# 📘 Учебник по CSS-селекторам и XPath для Web Scraping

## Для кого этот материал

Этот учебник предназначен для студентов, которые уже знают базовые CSS-селекторы и хотят научиться:
- увереннее искать элементы в HTML;
- понимать разницу между CSS и XPath;
- использовать оба подхода в задачах web scraping;
- писать более устойчивые и точные селекторы.

---

# 1. Зачем изучать и CSS, и XPath

При парсинге сайтов главная задача — **найти нужный элемент в HTML-документе**.

Для этого чаще всего используют два подхода:

- **CSS-селекторы**
- **XPath**

Оба инструмента позволяют находить элементы, но делают это по-разному.

## CSS-селекторы удобны, когда:
- у элементов есть классы, id, понятная вложенность;
- нужно быстро и просто выбрать элементы;
- вы используете `BeautifulSoup.select()` или `Selenium`.

## XPath удобен, когда:
- нужно искать элементы по тексту;
- нужно двигаться не только вниз по дереву, но и вверх;
- нужно выбирать элементы по сложным условиям;
- на странице мало удобных классов и атрибутов.

---

# 2. Краткое повторение HTML-структуры

Пример HTML:

```html
<html>
  <body>
    <div id="catalog">
      <div class="product featured" data-id="101">
        <h2 class="title">iPhone 15</h2>
        <p class="price">$999</p>
        <a href="/product/101">Open</a>
      </div>

      <div class="product" data-id="102">
        <h2 class="title">Samsung Galaxy</h2>
        <p class="price">$899</p>
        <a href="/product/102">Open</a>
      </div>
    </div>
  </body>
</html>
```

В этом HTML:
- `html`, `body`, `div`, `h2`, `p`, `a` — это **теги**
- `id`, `class`, `href`, `data-id` — это **атрибуты**
- текст внутри тегов — это **содержимое элементов**

---

# 3. CSS-селекторы: расширенный уровень

## 3.1 Поиск по тегу

```css
div
```

Найдет все элементы `<div>`.

---

## 3.2 Поиск по классу

```css
.product
```

Найдет все элементы с классом `product`.

---

## 3.3 Поиск по id

```css
#catalog
```

Найдет элемент с `id="catalog"`.

---

## 3.4 Тег + класс

```css
div.product
```

Найдет только `<div class="product">`.

---

## 3.5 Несколько классов сразу

```css
.product.featured
```

Найдет элемент, у которого одновременно есть оба класса:
- `product`
- `featured`

Это **не два разных элемента**, а **один элемент с двумя классами**.

---

## 3.6 Вложенность

```css
.product .title
```

Найдет все элементы с классом `title`, которые находятся **внутри** `.product`.

---

## 3.7 Прямой потомок

```css
.product > .title
```

Найдет `.title`, только если он является **непосредственным дочерним элементом** `.product`.

---

## 3.8 Соседние элементы

### Следующий сосед

```css
h2 + p
```

Найдет первый `<p>`, который идет сразу после `<h2>`.

### Все следующие соседи

```css
h2 ~ a
```

Найдет все `<a>`, которые идут после `<h2>` на том же уровне вложенности.

---

## 3.9 Работа с атрибутами

### Атрибут существует

```css
a[href]
```

### Точное совпадение

```css
div[data-id="101"]
```

### Атрибут содержит строку

```css
a[href*="/product/"]
```

### Атрибут начинается с

```css
a[href^="/product"]
```

### Атрибут заканчивается на

```css
a[href$="101"]
```

---

## 3.10 Псевдоклассы

### Первый дочерний элемент

```css
.product:first-child
```

### Последний дочерний элемент

```css
.product:last-child
```

### Элемент по номеру

```css
.product:nth-child(2)
```

### Четные элементы

```css
.product:nth-child(even)
```

### Нечетные элементы

```css
.product:nth-child(odd)
```

---

## 3.11 Выбор не по одному условию

### Несколько селекторов сразу

```css
h1, h2, h3
```

Найдет все `h1`, `h2`, `h3`.

### Исключение

```css
.product:not(.featured)
```

Найдет все `.product`, кроме тех, у которых есть класс `.featured`.

---

# 4. XPath: что это такое

**XPath** — это язык запросов к XML/HTML-документу.

Если CSS-селекторы больше похожи на "поиск по стилям и структуре", то XPath позволяет описывать путь к элементу и условия выбора гораздо точнее.

Примеры XPath:

```xpath
//div
```

Найти все `div`.

```xpath
//div[@class="product"]
```

Найти все `div` с классом `product`.

```xpath
//div[@data-id="101"]
```

Найти `div`, у которого `data-id="101"`.

---

# 5. Базовый синтаксис XPath

## 5.1 Абсолютный путь

```xpath
/html/body/div
```

Идет строго по всей структуре страницы.

Такой способ обычно **неустойчивый**, потому что малейшее изменение HTML ломает путь.

---

## 5.2 Относительный путь

```xpath
//div
```

Ищет `div` в любом месте документа.

Это гораздо удобнее в scraping-задачах.

---

## 5.3 Поиск по атрибуту

```xpath
//a[@href]
```

Найдет все ссылки, у которых есть атрибут `href`.

```xpath
//div[@id="catalog"]
```

Найдет элемент с `id="catalog"`.

---

## 5.4 Поиск по тексту

```xpath
//h2[text()="iPhone 15"]
```

Найдет `h2`, текст которого ровно `"iPhone 15"`.

Очень важное отличие от CSS:  
**XPath умеет искать по тексту напрямую, CSS — нет.**

---

## 5.5 Частичное совпадение текста

```xpath
//h2[contains(text(), "iPhone")]
```

---

## 5.6 Частичное совпадение атрибута

```xpath
//a[contains(@href, "/product/")]
```

---

## 5.7 Начало строки

```xpath
//a[starts-with(@href, "/product")]
```

---

## 5.8 Индексация

```xpath
(//div[@class="product"])[1]
```

Первый элемент.

```xpath
(//div[@class="product"])[2]
```

Второй элемент.

Важно: в XPath индексация начинается с **1**, а не с 0.

---

## 5.9 Условия внутри элемента

```xpath
//div[@class="product" and @data-id="101"]
```

Найдет `div`, который одновременно:
- имеет класс `product`
- имеет `data-id="101"`

---

# 6. Продвинутые возможности XPath

## 6.1 Поиск родителя

```xpath
//h2[@class="title"]/..
```

Вернет родительский элемент для `h2.title`.

Можно и так:

```xpath
//h2[@class="title"]/parent::div
```

Это очень полезно, когда вы нашли заголовок товара и хотите подняться к карточке целиком.

CSS-селекторы так не умеют.

---

## 6.2 Поиск предков

```xpath
//h2[@class="title"]/ancestor::div
```

Найдет всех предков `div`.

---

## 6.3 Поиск соседей

### Следующий сосед

```xpath
//h2/following-sibling::p
```

### Предыдущий сосед

```xpath
//p/preceding-sibling::h2
```

---

## 6.4 Поиск по нормализованному тексту

```xpath
//button[normalize-space(text())="Buy now"]
```

Полезно, когда в тексте есть лишние пробелы и переносы строк.

---

## 6.5 Комбинация условий

```xpath
//div[contains(@class, "product") and .//p[contains(@class, "price")]]
```

Найдет все карточки товара, внутри которых есть элемент цены.

---

# 7. CSS vs XPath

## 7.1 Когда CSS удобнее

CSS-селекторы обычно:
- короче;
- проще читаются;
- удобны для обычного поиска по классам, тегам, вложенности;
- отлично подходят для большинства стандартных страниц.

Пример:

```css
.product .title
```

---

## 7.2 Когда XPath удобнее

XPath лучше подходит, когда:
- нужен поиск по тексту;
- нужно идти вверх к родителю;
- нужна сложная логика условий;
- нужно искать относительно найденного элемента.

Пример:

```xpath
//button[contains(text(), "Купить")]
```

---

## 7.3 Таблица сравнения

| Задача | CSS | XPath |
|---|---|---|
| Найти по классу | ✅ Очень удобно | ✅ |
| Найти по id | ✅ Очень удобно | ✅ |
| Найти по тексту | ❌ Почти нет | ✅ Очень удобно |
| Подняться к родителю | ❌ Нет | ✅ |
| Найти по соседям | ⚠️ Ограниченно | ✅ |
| Простота чтения | ✅ | ⚠️ Иногда сложнее |
| Поддержка в BeautifulSoup | ✅ | ❌ |
| Поддержка в lxml | ✅ | ✅ |
| Поддержка в Selenium | ✅ | ✅ |

---

# 8. Примеры: один и тот же поиск через CSS и XPath

Пусть есть HTML:

```html
<div class="product featured" data-id="101">
    <h2 class="title">iPhone 15</h2>
    <p class="price">$999</p>
    <a href="/product/101">Open</a>
</div>
```

## Найти карточку товара

### CSS
```css
.product
```

### XPath
```xpath
//div[contains(@class, "product")]
```

---

## Найти заголовок товара

### CSS
```css
.product .title
```

### XPath
```xpath
//div[contains(@class, "product")]//h2[contains(@class, "title")]
```

---

## Найти ссылку товара

### CSS
```css
.product a[href]
```

### XPath
```xpath
//div[contains(@class, "product")]//a[@href]
```

---

## Найти карточку по тексту заголовка

### CSS
Сделать это напрямую нельзя.

### XPath
```xpath
//div[contains(@class, "product") and .//h2[text()="iPhone 15"]]
```

---

## Найти родительскую карточку от заголовка

### CSS
Нельзя подняться вверх.

### XPath
```xpath
//h2[text()="iPhone 15"]/ancestor::div[contains(@class, "product")]
```

---

# 9. BeautifulSoup: работа с CSS-селекторами

`BeautifulSoup` хорошо работает именно с CSS-селекторами.

## Пример

```python
from bs4 import BeautifulSoup

html = """
<div class="product featured" data-id="101">
    <h2 class="title">iPhone 15</h2>
    <p class="price">$999</p>
    <a href="/product/101">Open</a>
</div>
"""

soup = BeautifulSoup(html, "html.parser")

title = soup.select_one(".product .title").text
price = soup.select_one(".product .price").text
link = soup.select_one(".product a")["href"]

print(title)
print(price)
print(link)
```

## Важные методы

### `select()`
Возвращает список элементов.

```python
soup.select(".product")
```

### `select_one()`
Возвращает первый найденный элемент.

```python
soup.select_one(".title")
```

---

# 10. lxml: работа с XPath и CSS

Библиотека `lxml` поддерживает и XPath, и CSS.

## Пример с XPath

```python
from lxml import html

page = """
<div class="product featured" data-id="101">
    <h2 class="title">iPhone 15</h2>
    <p class="price">$999</p>
    <a href="/product/101">Open</a>
</div>
"""

tree = html.fromstring(page)

title = tree.xpath('//h2[@class="title"]/text()')[0]
price = tree.xpath('//p[@class="price"]/text()')[0]
link = tree.xpath('//a/@href')[0]

print(title)
print(price)
print(link)
```

## Пример с CSS в lxml

```python
from lxml import html

page = """
<div class="product featured" data-id="101">
    <h2 class="title">iPhone 15</h2>
    <p class="price">$999</p>
    <a href="/product/101">Open</a>
</div>
"""

tree = html.fromstring(page)

title = tree.cssselect(".title")[0].text_content()
price = tree.cssselect(".price")[0].text_content()
link = tree.cssselect("a")[0].get("href")

print(title)
print(price)
print(link)
```

---

# 11. Selenium: CSS и XPath в браузерной автоматизации

В Selenium можно использовать оба подхода.

## CSS

```python
from selenium.webdriver.common.by import By

title = driver.find_element(By.CSS_SELECTOR, ".product .title")
```

## XPath

```python
from selenium.webdriver.common.by import By

title = driver.find_element(By.XPATH, '//div[contains(@class, "product")]//h2')
```

## Когда в Selenium XPath особенно полезен

Например, когда нужно найти кнопку по тексту:

```python
button = driver.find_element(By.XPATH, '//button[contains(text(), "Купить")]')
```

Через CSS это сделать заметно сложнее или невозможно напрямую.

---

# 12. Как писать устойчивые селекторы

При scraping важно не просто "найти элемент", а найти его так, чтобы код не ломался после первого изменения верстки.

## Хорошие признаки устойчивого селектора

- есть `id`, если он стабильный;
- есть понятный класс, связанный со смыслом;
- есть специальные атрибуты вроде `data-id`, `data-test`, `data-qa`;
- селектор не слишком длинный.

## Плохие признаки

- слишком длинная цепочка вроде:
  ```css
  body > div > div > div > ul > li > span
  ```
- использование случайных автогенерируемых классов;
- опора на номер элемента, если порядок может меняться;
- абсолютный XPath.

## Лучше так

```css
.product .title
```

или

```xpath
//div[contains(@class, "product")]//h2[contains(@class, "title")]
```

## Хуже так

```xpath
/html/body/div[2]/div[4]/div[1]/h2
```

---

# 13. Типичные ошибки студентов

## Ошибка 1. Путают пробел и отсутствие пробела

```css
.product .price
```

Это `.price` внутри `.product`.

```css
.product.price
```

Это один элемент, у которого два класса:
- `product`
- `price`

---

## Ошибка 2. Путают `.` и `#`

- `.title` — класс
- `#title` — id

---

## Ошибка 3. Думают, что XPath и CSS одинаковые

Они решают похожие задачи, но возможности у них разные.

---

## Ошибка 4. Используют слишком общий селектор

```css
div
```

Он часто находит слишком много лишнего.

---

## Ошибка 5. Используют абсолютный XPath

```xpath
/html/body/div/div/div[2]/span
```

Такой путь очень хрупкий.

---

## Ошибка 6. Не проверяют результат

Нужно всегда проверять:
- что элемент вообще найден;
- что текст не пустой;
- что селектор не захватывает лишние элементы.

---

# 14. Практика

## Задание 1

HTML:

```html
<div class="card">
    <h3 class="name">Alice</h3>
    <span class="age">25</span>
</div>
<div class="card">
    <h3 class="name">Bob</h3>
    <span class="age">30</span>
</div>
```

### Нужно:
1. Найти все карточки через CSS.
2. Найти все имена через CSS.
3. Найти возраст Bob через XPath.

---

## Задание 2

HTML:

```html
<ul class="menu">
    <li><a href="/home">Home</a></li>
    <li><a href="/catalog">Catalog</a></li>
    <li><a href="/contacts">Contacts</a></li>
</ul>
```

### Нужно:
1. Найти все ссылки через CSS.
2. Найти ссылку на `catalog` через CSS.
3. Найти ссылку, у которой текст `Contacts`, через XPath.

---

## Задание 3

HTML:

```html
<div class="product" data-id="501">
    <h2 class="title">Notebook</h2>
    <button>Buy now</button>
</div>
```

### Нужно:
1. Найти кнопку через CSS.
2. Найти кнопку по тексту через XPath.
3. Найти родительский `div.product` от кнопки через XPath.

---

# 15. Ответы к практике

## Задание 1

### CSS: все карточки
```css
.card
```

### CSS: все имена
```css
.card .name
```

### XPath: возраст Bob
```xpath
//div[contains(@class, "card") and .//h3[text()="Bob"]]//span[contains(@class, "age")]
```

---

## Задание 2

### CSS: все ссылки
```css
.menu a
```

### CSS: ссылка catalog
```css
a[href="/catalog"]
```

### XPath: ссылка Contacts по тексту
```xpath
//a[text()="Contacts"]
```

---

## Задание 3

### CSS: кнопка
```css
.product button
```

### XPath: кнопка по тексту
```xpath
//button[text()="Buy now"]
```

### XPath: родительская карточка
```xpath
//button[text()="Buy now"]/parent::div
```

---

# 16. Мини-шпаргалка

## CSS

```css
.tag              /* по тегу */
.class            /* по классу */
#id               /* по id */
.parent .child    /* любой потомок */
.parent > .child  /* прямой потомок */
a[href]           /* есть атрибут */
a[href*="login"]  /* содержит */
a[href^="/"]      /* начинается с */
a[href$=".pdf"]   /* заканчивается на */
.item:first-child
.item:last-child
.item:nth-child(2)
.item:not(.active)
```

## XPath

```xpath
//div
//div[@class="product"]
//a[@href]
//h2[text()="Title"]
//h2[contains(text(), "Title")]
//a[contains(@href, "catalog")]
//button[starts-with(@id, "buy")]
(//div[@class="product"])[1]
//h2/parent::div
//h2/ancestor::div
//h2/following-sibling::p
//button[normalize-space(text())="Buy now"]
```

---

# 17. Что выбрать на практике

## Используйте CSS, если:
- задача простая;
- есть классы и id;
- вы парсите через BeautifulSoup;
- хочется сделать код короче и понятнее.

## Используйте XPath, если:
- нужен поиск по тексту;
- нужно идти к родителю или предкам;
- нужен более гибкий и мощный запрос;
- вы работаете с Selenium или lxml.

## Хорошая стратегия
Уметь пользоваться **обоими инструментами** и выбирать тот, который проще и надежнее в конкретной задаче.

---

# 18. Итог

CSS-селекторы и XPath — это два главных инструмента поиска элементов в HTML.

Важно не просто запомнить синтаксис, а понять:
- как устроено DOM-дерево;
- как связаны элементы;
- какой селектор будет надежным;
- когда лучше выбрать CSS, а когда XPath.

Для web scraping этого достаточно, чтобы уверенно:
- доставать названия;
- цены;
- ссылки;
- карточки товаров;
- кнопки;
- таблицы и списки.

---

# 19. Что изучать дальше

После этой темы логично переходить к:
1. парсингу реальных сайтов;
2. обработке ошибок при поиске элементов;
3. динамическим страницам и JavaScript;
4. Selenium / Playwright;
5. обходу пагинации;
6. извлечению данных из таблиц, карточек и списков;
7. построению полноценного парсера.

---

# 20. Домашнее задание

1. Найдите любой интернет-магазин с простой версткой.
2. Через DevTools определите селекторы для:
   - названия товара;
   - цены;
   - ссылки на товар;
   - изображения.
3. Запишите для каждого элемента:
   - CSS-селектор;
   - XPath.
4. Подумайте, какой из двух вариантов более устойчивый и почему.

---

Удачи в практике.  
Самый быстрый способ освоить селекторы — не просто читать, а постоянно открывать HTML и пытаться находить элементы разными способами.

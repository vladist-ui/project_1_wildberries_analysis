import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def clean_symbols(str_) -> float:
    str_ = str_.replace('\u2006', ' ')
    first_point = str_ .find('.')
    if first_point != -1:
        str_ = str_[:first_point + 2]
    str_  = re.sub(r"[^\d.-]", "", str_.replace(",", "."))
    
    return float(str_)

def cuter(str_):
    if str_[1] == ".":
        return str_[:3], 3
    else:
        str_[0], 0

def pars_wildberries(req, driver, df):
    # Подождём прогрузки страницы
    time.sleep(0.7)
    
    # Найдём на странице окно поиска товара
    search_input = driver.find_element(By.ID, "searchInput")
    # Нажмём на неё
    search_input.click()
    # Очистим строку поиска товара
    search_input.clear()
    # Введём запрос
    search_input.send_keys(req)
    # Нажмём кнопку ввода
    search_input.send_keys(Keys.RETURN)

    html_texts = []

    
    for _ in range(20):
        time.sleep(0.5)
        
        # Скролим вниз
        for __ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            driver.execute_script("window.scrollBy(0, -200)")
            time.sleep(0.5)

        # Добавим в список
        html_text = driver.page_source
        html_texts.append(html_text)

         
        # Перелистываем страницу
        soup = BeautifulSoup(html_text, "html.parser")
        next_link = soup.find('a', class_='pagination-next pagination__next j-next-page').get('href')
        driver.get(next_link)


    for html_text in html_texts:
        # Найдём карточки товаров
        soup = BeautifulSoup(html_text, "html.parser") 
        items = soup.find_all('article', class_='product-card')
        
        for item in items:
            try:
                # Название товара
                title = item.find('a', class_='product-card__link j-card-link j-open-full-product-card').get('aria-label')
                # Цена
                price = item.find('div', class_='product-card__price price').text.strip()
                price = clean_symbols(price[:price.find("₽")])
                # Рейтинг
                rating, len_ = cuter(item.find('div', class_='product-card__rating-wrap').text.strip().replace(',', '.'))
                # Кол-во отзывов
                reviews = clean_symbols(item.find('div', class_='product-card__rating-wrap').text.strip()[len_:])
                # Ссылка на товар
                link = item.find('a', class_='product-card__link j-card-link j-open-full-product-card').get('href')
                full_link = f"https://market.yandex.ru{link}" if link.startswith('/') else link
            except:
                continue
            df.loc[len(df)] = [title, price, rating, reviews, full_link, req]
        
    return df

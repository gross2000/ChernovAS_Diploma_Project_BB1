"""Функционал Web-скрапинга"""
from loguru import logger
from bs4 import BeautifulSoup
import re
import urllib.request
from urllib.error import URLError, HTTPError

class Scraper():
    """Класс для веб-скрапинга"""
    def __init__(self, site, max_pages):
        self.site = site
        self.max_pages = max_pages
        self.data = {'link': [],
                    'name': [],
                    'price': [],
                    'rating': [],
                    'description': [],
                    'manual': [],
                    'country': []
                    }
    logger.add("scraper.log", rotation="1 MB", level="DEBUG", backtrace=True, diagnose=True)

    def scrape(self):
        """Стартовый скрапинг стартовой страницы сайта"""
        for page in range(1, self.max_pages + 1):
            url = f"{self.site}?p={page}"
            logger.info(f"Сканирование страницы: {url}")
            r = urllib.request.urlopen(url)
            html = r.read()
            parser = "html.parser"
            sp = BeautifulSoup(html, parser)
            for tag in sp.find_all("article"):
                link = tag.find('a')['href']
                logger.info(f"Link: {link}")
                self.scrape_product(link)

    def scrape_product(self, product_link):
        """Дополнительные действия для сбора данных конкретного товара"""
        base_url =  f'{self.site}'
        mod_url = re.sub(r'/parfjumerija', '', base_url)
        product_url = f'{mod_url}{product_link}'
        logger.info(f'Сканирование страницы товара: {product_url}')
        try:
            r = urllib.request.urlopen(product_url)
            html = r.read()
            parser = 'html.parser'
            sp = BeautifulSoup(html, parser)
            self.data['link'].append(product_url)

            # запись name в словарь
            name_text = self.get_name(sp)
            self.data['name'].append(name_text)

            # запись price в словарь
            price_text = self.get_price(sp)
            self.data['price'].append(price_text)

            # запись description в словарь
            description_text = self.get_description(sp)
            self.data['description'].append(description_text)

            # запись manual в словарь
            manual_text = self.get_manual(sp)
            self.data['manual'].append(manual_text)

            # запись country в словарь
            country = self.get_country(sp)
            self.data['country'].append(country)

            # запись country в словарь
            rating_text = self.get_rating(product_url, mod_url)
            self.data['rating'].append(rating_text)

        except Exception as e:
            logger.error(f"Ошибка при получении страницы товара {product_url}: {e}")

    def get_data(self):
        """Метод для получения словаря"""
        return self.data

    def get_name(self, sp):
        """Метод для сбора наименования товара"""
        target_div = sp.find('div', {'value': 'Description_0', 'text': 'описание'})
        if target_div:
            parent = sp.find('div', {'value': 'Description_0', 'text': 'описание'})
            name = parent.find_next('div')
            name_text = name.get_text(strip=True)
            logger.info(f'Наименование товара: {name_text}')
            return name_text
        else:
            name_text = 'не указано'
            logger.info(f'Наименование товара: {name_text}')
            return name_text

    def get_price(self, sp):
        """Метод для сбора цены товара"""
        target_div = sp.find('div', itemprop="priceSpecification")
        if target_div:
            parent = sp.find('div', itemprop="priceSpecification")
            price = parent.find_next_sibling('div')
            if price: # Проверка на None
                price_text = price.get_text(strip=True)
                price_text = re.search(r'\d{1,3}\s?\d{1,3}₽', price_text).group(0)
                logger.info(f'Цена товара: {price_text}')
                return price_text
            else:
                return 'не указана'
        else:
            price_text = 'не указана'
            logger.info(f'Цена товара: {price_text}')
            return price_text

    def get_description(self,sp):
        """Метод для сбора описаения товара"""
        description = sp.find('div', itemprop='description')
        if description:
            description_text = description.get_text(separator=' ', strip=True)
            description_text = re.sub(r'\n', '', description_text)
            logger.info(f'Описание товара: {description_text}')
            return description_text
        else:
            description_text = 'не указано'
            logger.info(f'Описание товара: {description_text}')
            return description_text

    def get_manual(self, sp):
        """Метод для сбора инструкции товара"""
        target_div = sp.find('div', {'value': 'Text_1', 'text': 'применение'})
        if target_div:
            parent = sp.find('div', {'value': 'Text_1', 'text': 'применение'})
            manual = parent.find('div')
            manual_text = manual.get_text(separator=' ', strip=True) if manual else ''
            logger.info(f'Инструкция по применению: {manual_text}')
            return manual_text
        else:
            manual_text = 'не указана'
            logger.info(f'Инструкция по применению: {manual_text}')
            return manual_text

    def get_country(self, sp):
        """Метод для сбора информации о стране-производителе товара"""
        target_div = sp.find('div', {'value': 'Text_3', 'text': 'Дополнительная информация'})
        if target_div:
            parent = sp.find('div', {'value': 'Text_3', 'text': 'Дополнительная информация'})
            tag = parent.find('div')
            tag_text = tag.get_text(separator=' ', strip=True) if tag else ''
            country = re.findall(r',\s([^,]*).?$', tag_text)
            country = country[0]
            logger.info(f'Страна-производитель: {country}')
            return country
        else:
            country = 'не указана'
            logger.info(f'Страна-производитель: {country}')
            return country

    def get_rating(self, product_url, mod_url):
        """Метод для сбора информации о рейтинге товара"""
        try:
            # Извлекаем ID продукта из URL
            match = re.search(r'/(\d+)-.*$', product_url)
            if match:
                rating_url = f'{mod_url}/review/product/{match.group(1)}'
                logger.info(f'Открываем страницу рейтинга: {rating_url}')
            else:
                raise ValueError(f'Не удалось извлечь рейтинг из URL: {product_url}')

            # Выполняем HTTP-запрос к странице рейтинга
            try:
                r = urllib.request.urlopen(rating_url)
                html = r.read()
            except HTTPError as e:
                logger.error(f'HTTP ошибка при открытии страницы: {e.code} {e.reason}')
                return None
            except URLError as e:
                logger.error(f'Ошибка доступа к URL: {e.reason}')
                return None

            parser = 'html.parser'
            sp = BeautifulSoup(html, parser)

            # Ищем элемент с рейтингом
            rating = sp.find('div', itemprop='ratingValue')
            if rating:
                rating_text = rating.get_text(strip=True)
                logger.info(f'Рейтинг: {rating_text}')
                return rating_text
            else:
                rating_text = 'не указан'
                logger.info(f'Рейтинг: {rating_text}')
                return rating_text

        except ValueError as e:
            logger.error(f'Ошибка: {e}')
            return None
        except Exception as e:
            logger.error(f'Неожиданная ошибка: {e}')
            return None
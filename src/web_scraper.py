"""Функционал Web-скрапинга"""
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import re
import urllib.request


class AbstractScraper(ABC):
    @abstractmethod
    def scrape(self):
        pass

    @abstractmethod
    def scrape_product(self, product_link):
        pass

    @abstractmethod
    def get_data(self):
        pass


class Scraper(AbstractScraper):

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

    def scrape(self):

        """Стартовый скрапинг стартовой страницы сайта"""
        for page in range(1, self.max_pages + 1):
            url = f"{self.site}?p={page}"
            print(f"Сканирование страницы: {url}")
            r = urllib.request.urlopen(url)
            html = r.read()
            parser = "html.parser"
            sp = BeautifulSoup(html,parser)
            for tag in sp.find_all("article"):
                link = tag.find('a')['href']
                print(f'Link: {link}')
                self.scrape_product(link)


    def scrape_product(self, product_link):

        """Дополнительные действия для сбора данных конкретного товара"""
        base_url =  f'{self.site}'
        mod_url = re.sub(r'/parfjumerija', '', base_url)
        product_url = f'{mod_url}{product_link}'
        print(f'Сканирование страницы товара: {product_url}')
        r = urllib.request.urlopen(product_url)
        html = r.read()
        parser = 'html.parser'
        sp = BeautifulSoup(html, parser)
        self.data['link'].append(product_url)

        # Наименование
        target_div = sp.find('div', {'value': 'Description_0', 'text': 'описание'})
        if target_div:
            parent = sp.find('div', {'value': 'Description_0', 'text': 'описание'})
            name = parent.find_next('div')
            name_text = name.get_text(strip=True)
            print(f'Наименование товара: {name_text}')
            self.data['name'].append(name_text)
        else:
            name_text = 'не указано'
            self.data['name'].append(name_text)

        # Цена
        target_div = sp.find('div', itemprop="priceSpecification")
        if target_div:
            parent = sp.find('div', itemprop="priceSpecification")
            price = parent.find_next_sibling('div')
            price_text = price.get_text(strip=True)
            print(f'Цена товара: {re.search(r'\d{1,3}\s?\d{1,3}₽', price_text).group(0)}')
            self.data['price'].append(re.search(r'\d{1,3}\s?\d{1,3}₽', price_text).group(0))
        else:
            price_text = 'не указана'
            self.data['price'].append(price_text)


        # Описание
        description = sp.find('div', itemprop='description')
        if description:
            description_text = description.get_text(separator=' ', strip=True)
            description_text = re.sub(r'\n', '', description_text)
            print(f'Описание товара: {description_text}')
            self.data['description'].append(description_text)
        else:
            description_text = 'не указано'
            self.data['description'].append(description_text)


        # Инструкция по применению
        target_div = sp.find('div', {'value': 'Text_1', 'text': 'применение'})
        if target_div:
            parent = sp.find('div', {'value': 'Text_1', 'text': 'применение'})
            manual = parent.find('div')
            manual_text = manual.get_text(separator=' ', strip=True) if manual else ''
            print(f'Инструкция по применению: {manual_text}')
            self.data['manual'].append(manual_text)
        else:
            manual_text = 'не указана'
            self.data['manual'].append(manual_text)


        # Страна-производитель
        target_div = sp.find('div', {'value': 'Text_3', 'text': 'Дополнительная информация'})
        if target_div:
            parent = sp.find('div', {'value': 'Text_3', 'text': 'Дополнительная информация'})
            tag = parent.find('div')
            tag_text = tag.get_text(separator=' ', strip=True) if tag else ''
            country = re.findall(r',\s([^,]*).?$', tag_text)
            country = country[0]
            print(f'Страна-производитель: {country}')
            self.data['country'].append(country)
        else:
            country = 'не указана'
            self.data['country'].append(country)


        # Рейтинг
        try:
            match = re.search(r'/(\d+)-.*$', product_url)
            if match:
                rating_url = f'{mod_url}/review/product/{match.group(1)}'
                print(f'Открываем страницу рейтинга: {rating_url}')
            else:
                raise ValueError(f'Не удалось извлечь рейтинг из URL: {product_url}')
            r = urllib.request.urlopen(rating_url)
            html = r.read()
            parser = 'html.parser'
            sp = BeautifulSoup(html, parser)
            rating = sp.find('div', itemprop='ratingValue')
            if rating:
                rating_text = rating.get_text(strip=True)
                print(f'Рейтинг: {rating_text}')
                self.data['rating'].append(rating_text)
            else:
                rating_text = 'не указан'
                self.data['rating'].append(rating_text)
        except ValueError as e:
            print(f'Отсутствуют данные')

    def get_data(self):
        return self.data
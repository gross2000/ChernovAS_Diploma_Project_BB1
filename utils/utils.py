# Здесь первый вариант кода (оставил для справки)

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

    def __init__(self, site, max_pages):
        self.site = site
        self.max_pages = max_pages
        self.data = {'link': [],
                    'name': [],
                    'price': [],
                    'raiting': [],
                    'description': [],
                    'manual': [],
                    'country': []
                    }

    def scrape(self):

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

        base_url =  f"{self.site}"
        mod_url = re.sub(r'/parfjumerija', '', base_url)
        product_url = f"{mod_url}{product_link}"
        print(f"Сканирование страницы товара: {product_url}")
        r = urllib.request.urlopen(product_url)
        html = r.read()
        parser = "html.parser"
        sp = BeautifulSoup(html, parser)
        self.data['link'].append(product_url)

        # Дополнительные действия для сбора данных о товаре:
        # Наименование
        name = sp.find('div', class_='F8wxT')
        name_text = name.get_text(strip=True)
        print(f'Наименование товара: {name_text}')
        self.data['name'].append(name_text)

        # Цена
        price = sp.find('div', class_='-9ePq Vz+QM')
        price_text = price.get_text(strip=True)
        print(f'Цена товара: {price_text}')
        self.data['price'].append(price_text)

        # Описание
        description = sp.find('div', class_='MXdIX', itemprop='description')
        description_text = description.get_text(separator=' ', strip=True) if description else ''
        description_text = re.sub(r'\n','', description_text)
        print(f'Описание товара: {description_text}')
        self.data['description'].append(description_text)

        # Инструкция по применению
        target_div = sp.find('div', {'value': 'Text_1', 'text': 'применение'})
        if target_div:
            parent = sp.find('div', {'value': 'Text_1', 'text': 'применение'})
            manual = parent.find('div', class_='MXdIX')
            manual_text = manual.get_text(separator=' ', strip=True) if manual else ''
            print(f'Инструкция по применению: {manual_text}')
            self.data['manual'].append(manual_text)
        else:
            manual_text = ''

        # Страна-производитель
        target_div = sp.find('div', {'value': 'Text_3', 'text': 'Дополнительная информация'})
        if target_div:
            parent = sp.find('div', {'value': 'Text_3', 'text': 'Дополнительная информация'})
            tag = parent.find('div', class_='MXdIX')
            tag_text = tag.get_text(separator=' ', strip=True) if tag else ''
            country = re.findall(r',\s([^,]*).?$', tag_text)
            country = country[0]
            print(f'Страна-производитель: {country}')
            self.data['country'].append(country)
        else:
            country = ''


    def get_data(self):
        return self.data

        # Варик чат
        # ====================================================================================================
        # # Наименование
        # target_div = sp.find('div', {'value': 'Description_0', 'text': 'описание'})
        # if target_div:
        #     name = target_div.find_next_sibling('div')
        #     if name:  # Проверяем, найден ли тег
        #         name_text = name.get_text(strip=True)
        #         print(f'Наименование товара: {name_text}')
        #         self.data['name'].append(name_text)
        #     else:
        #         self.data['name'].append('не указана')
        # else:
        #     name_text = 'не указана'
        #     self.data['name'].append(name_text)
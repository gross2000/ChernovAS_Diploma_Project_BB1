from bs4 import BeautifulSoup
import re
import urllib.request


class Scraper:

    def __init__(self, site, max_pages):
        self.site = site
        self.max_pages = max_pages

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

        # Дополнительные действия для сбора данных о товаре:
        # Наименование
        name = sp.find('div', class_='F8wxT')
        name_text = name.get_text(strip=True)
        print(f'Наименование товара: {name_text}')

        # Цена
        price = sp.find('div', class_='-9ePq Vz+QM')
        price_text = price.get_text(strip=True)
        print(f'Цена товара: {price_text}')

        # Описание
        description = sp.find('div', class_='MXdIX', itemprop='description')
        description_text = description.get_text(separator=' ', strip=True) if description else ''
        description_text = re.sub(r'\n','', description_text)
        print(f'Описание товара: {description_text}')


        # Инструкция по применению
        target_div = sp.find('div', {'value': 'Text_1', 'text': 'применение'})
        if target_div:
            parent = sp.find('div', {'value': 'Text_1', 'text': 'применение'})
            manual = parent.find('div', class_='MXdIX')
            manual_text = manual.get_text(separator=' ', strip=True) if manual else ''
            print(f'Инструкция по применению: {manual_text}')
        else:
            manual_text = ''


        # Страна-производитель
        target_div = sp.find('div', {'value': 'Text_3', 'text': 'Дополнительная информация'})
        if target_div:
            parent = sp.find('div', {'value': 'Text_3', 'text': 'Дополнительная информация'})
            tag = parent.find('div', class_='MXdIX')
            tag_text = tag.get_text(separator=' ', strip=True) if tag else ''
            country = re.findall(r',\s([^,]*).?$', tag_text)
            print(f'Страна-производитель: {country[0]}')
        else:
            country = ''
"""Тестовая часть для функционала Web-скрапинга"""
from unittest.mock import patch, MagicMock
from src.web_scraper import Scraper
import unittest
from bs4 import BeautifulSoup

class TestScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper('http://example.com', 1)
        assert isinstance(self.scraper.data, dict), "data должен быть словарем."
        assert len(self.scraper.data['link']) == 0, "Список ссылок должен быть пустым."
        assert len(self.scraper.data['name']) == 0, "Список названий должен быть пустым."
        assert len(self.scraper.data['price']) == 0, "Список цен должен быть пустым."
        assert len(self.scraper.data['rating']) == 0, "Список рейтингов должен быть пустым."
        assert len(self.scraper.data['description']) == 0, "Список описаний должен быть пустым."
        assert len(self.scraper.data['manual']) == 0, "Список мануалов должен быть пустым."
        assert len(self.scraper.data['country']) == 0, "Список стран должен быть пустым."

        # Подготавливаем HTML-код для тестов
        self.html_with_price = '''
           <div>
                <div itemprop="priceSpecification">
                    <div>
                        1000
                            <span>₽</span>
                    </div>
                </div>
           </div>        
           '''

        self.html_without_price = '''
            <div itemprop="priceSpecification">
                <div>Цена</div>
            </div>
            '''

        self.html_with_description = '''
            <div itemprop="description">
                Это прекрасный товар с отличными характеристиками.
            </div>
            '''

        self.html_without_description = '''
            <div></div>            
            '''

        self.html_with_manual = '''
            <div value="Text_1" text="применение">
                <div>
                    Инструкция по применению товара
                </div>
            </div>
            '''

        self.html_without_manual = '''<div></div>'''

        self.html_with_country = '''
            <div value="Text_3" text="Дополнительная информация">
                <div>
                    Страна-производитель товара, Лапландия
                </div>
            </div>
            '''

        self.html_without_country = '''<div></div>'''


    @patch('urllib.request.urlopen')
    def test_scrape(self, mock_urlopen):
        # Настроим возврат для mock объекта
        mock_response = MagicMock()
        mock_response.read.return_value = b'<html><body><article><a href="/product1"></a></article></body></html>'
        mock_urlopen.return_value = mock_response

        self.scraper.scrape()

        # Проверяем, что данные были добавлены
        self.assertTrue(len(self.scraper.data['link']) > 0)
        self.assertIn("http://example.com/product1", self.scraper.data['link'])

    @patch('urllib.request.urlopen')
    def test_scrape_product(self, mock_urlopen):
        # Настраиваем возврат для mock объекта
        mock_response = MagicMock()
        mock_response.read.return_value = b'<html><body><h1>Product Title</h1></body></html>'
        mock_urlopen.return_value = mock_response

        self.scraper.scrape_product('/product1')

        # Проверяем, что URL продукта был добавлен
        self.assertIn("http://example.com/product1", self.scraper.data['link'])

    @patch('urllib.request.urlopen')
    def test_scrape_with_no_articles(self, mock_urlopen):
        # Настраиваем возврат с отсутствующими товарами
        mock_response = MagicMock()
        mock_response.read.return_value = b'<html><body></body></html>'
        mock_urlopen.return_value = mock_response

        self.scraper.scrape()

        # Убеждаемся, что список ссылок пуст
        self.assertEqual(len(self.scraper.data['link']), 0)

    def test_get_name(self):
        scraper = Scraper("http://example.com", 1)
        mock_soup = BeautifulSoup(
            "<html><body><div value='Description_0' text='описание'><div>Test Product</div></div></body></html>",
            'html.parser')

        name = scraper.get_name(mock_soup)

        self.assertEqual(name, "Test Product")

    def test_get_name_no_product(self):
        scraper = Scraper("http://example.com", 1)
        mock_soup = BeautifulSoup("<html><body></body></html>", 'html.parser')

        name = scraper.get_name(mock_soup)

        self.assertEqual(name, "не указано")

    def test_get_data(self):
        scraper = Scraper("http://example.com", 1)
        expected_data = {
            'link': [],
            'name': [],
            'price': [],
            'rating': [],
            'description': [],
            'manual': [],
            'country': []
        }

        self.assertEqual(scraper.get_data(), expected_data)


    @patch('urllib.request.urlopen')
    @patch('re.search')
    def test_get_rating_success(self, mock_search, mock_urlopen):
        # Подготовка mock-объектов
        mock_search.return_value = MagicMock(group=lambda x: '12345')  # Имитация успешного поиска
        mock_html = b'''
                <html>
                    <body>
                        <div itemprop="ratingValue">4.5</div>
                    </body>
                </html>
            '''
        mock_urlopen.return_value.read.return_value = mock_html  # Имитация ответа от сервера

        result = self.scraper.get_rating("http://example.com/product/12345", "http://example.com")
        self.assertEqual(result, "4.5")  # Проверка правильного извлеченного значения



    @patch('urllib.request.urlopen')
    @patch('re.search')
    def test_get_rating_no_rating(self, mock_search, mock_urlopen):
        # Подготовка mock-объектов
        mock_search.return_value = MagicMock(group=lambda x: '12345')
        mock_html = b'''
                <html>
                    <body>
                        <div></div>
                    </body>
                </html>
            '''
        mock_urlopen.return_value.read.return_value = mock_html  # Имитация ответа от сервера

        result = self.scraper.get_rating("http://example.com/product/12345", "http://example.com")
        self.assertEqual(result, "не указан")  # Проверка случая, когда рейтинг не указан

    @patch('urllib.request.urlopen')
    @patch('re.search')
    def test_get_rating_http_error(self, mock_search, mock_urlopen):
        # Имитация ошибки HTTP
        mock_search.return_value = MagicMock(group=lambda x: '12345')
        mock_urlopen.side_effect = Exception('HTTP Error')

        result = self.scraper.get_rating("http://example.com/product/12345", "http://example.com")
        self.assertEqual(result, None)  # Проверка случай, когда возникает ошибка HTTP


    def test_get_price_success(self):
        self.scraper = Scraper("http://example.com", 1)
        self.bs_with_price = BeautifulSoup(self.html_with_price, 'html.parser')
        price = self.scraper.get_price(self.bs_with_price)
        assert price

    def test_get_price_no_price(self):
        self.scraper = Scraper("http://example.com", 1)
        self.bs_without_price = BeautifulSoup(self.html_without_price, 'html.parser')
        price = self.scraper.get_price(self.bs_without_price)
        self.assertEqual(price, "не указана")  # Ожидаемое значение

    def test_get_description_success(self):
        self.scraper = Scraper("http://example.com", 1)
        self.bs_with_description = BeautifulSoup(self.html_with_description, 'html.parser')
        description = self.scraper.get_description(self.bs_with_description)
        self.assertEqual(description, "Это прекрасный товар с отличными характеристиками.")  # Ожидаемое значение

    def test_get_description_no_description(self):
        self.scraper = Scraper("http://example.com", 1)
        self.bs_without_description = BeautifulSoup(self.html_without_description, 'html.parser')
        description = self.scraper.get_description(self.bs_without_description)
        self.assertEqual(description, "не указано")  # Ожидаемое значение

    def test_get_manual_success(self):
        self.scraper = Scraper("http://example.com", 1)
        self.bs_with_manual = BeautifulSoup(self.html_with_manual, 'html.parser')
        manual = self.scraper.get_manual(self.bs_with_manual)
        self.assertEqual(manual, "Инструкция по применению товара")  # Ожидаемое значение

    def test_get_manual_no_manual(self):
        self.scraper = Scraper("http://example.com", 1)
        self.bs_without_manual = BeautifulSoup(self.html_without_manual, 'html.parser')
        manual = self.scraper.get_manual(self.bs_without_manual)
        self.assertEqual(manual, "не указана")  # Ожидаемое значение

    def test_get_country_success(self):
        self.scraper = Scraper("http://example.com", 1)
        self.bs_with_country = BeautifulSoup(self.html_with_country, 'html.parser')
        country = self.scraper.get_country(self.bs_with_country)
        self.assertEqual(country, "Лапландия")  # Ожидаемое значение

    def test_get_no_country(self):
        self.scraper = Scraper("http://example.com", 1)
        self.bs_without_country = BeautifulSoup(self.html_without_country, 'html.parser')
        country = self.scraper.get_manual(self.bs_without_country)
        self.assertEqual(country, "не указана")  # Ожидаемое значение



if __name__ == '__main__':
    unittest.main()
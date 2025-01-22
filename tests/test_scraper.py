"""Тестовая часть для функционала Web-скрапинга"""
import pytest
from unittest.mock import patch, MagicMock
from src.web_scraper import Scraper
from unittest import mock
from bs4 import BeautifulSoup
import re

@pytest.fixture
def scraper():
    return Scraper("http://example.com", 1)

def test_init(scraper):
    assert scraper.site == "http://example.com"
    assert scraper.max_pages == 1
    assert scraper.data == {'link': [], 'name': [], 'price': [], 'rating': [],
                             'description': [], 'manual': [], 'country': []}


@mock.patch('urllib.request.urlopen')
@mock.patch('bs4.BeautifulSoup')
def test_scrape(mock_bs4, mock_urlopen, scraper):
    # Настраиваем моки
    mock_html = "<html><body><article><a href='/product/1'></a></article></body></html>"
    mock_urlopen.return_value.read.return_value = mock_html.encode('utf-8')
    mock_bs4.return_value.find_all.return_value = [MagicMock()]

    # Выполняем метод
    scraper.scrape()

    mock_urlopen.assert_called_once_with("http://example.com?p=1")
    assert scraper.data['link'] == []  # scrape_product не вызывается


@mock.patch('urllib.request.urlopen')
@mock.patch('bs4.BeautifulSoup')
def test_scrape_product(mock_bs4, mock_urlopen, scraper):
    scraper.data = {'link': [], 'name': [], 'price': [], 'rating': [],
                        'description': [], 'manual': [], 'country': []}

    # Настраиваем моки
    mock_urlopen.side_effect = [
    MagicMock(read=lambda: b"<html><body><article><a href='/product/1'></a></article></body></html>"),
    MagicMock(read=lambda: "<html><body><div value='Description_0'>описание</div><div>Товар 1</div><div itemprop='priceSpecification'>1000₽</div></body></html>".encode(
    'utf-8'))]

    mock_bs4.return_value.find.return_value = MagicMock()
    mock_bs4.return_value.find_next.return_value = MagicMock(get_text=lambda strip: "Товар 1")

    # Выполняем метод
    scraper.scrape_product('/product/1')

    assert len(scraper.data['link']) == 1
    assert scraper.data['name'][0] == "Товар 1"
    assert scraper.data['price'][0] == "1000₽"
    assert scraper.data['description'][0] == 'не указано'  # По умолчанию
    assert scraper.data['manual'][0] == 'не указана'  # По умолчанию

if __name__ == "__main__":
    pytest.main()
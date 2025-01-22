from src.web_scraper import Scraper
from src.csv_class import CSVSaver


def scrapnwrite():
    """ Функция вызова сервиса веб-скрапинга и записи в данных в файл CSV"""
    site = "https://goldapple.ru/parfjumerija"
    scraper = Scraper(site, 1)
    scraper.scrape()
    data = scraper.get_data()
    print(data)
    csv_saver = CSVSaver()
    csv_saver.write_data(data)


def waste_csv():
    """ Функция удаления данных из файла CSV"""
    csv_saver = CSVSaver()
    csv_saver.del_data()
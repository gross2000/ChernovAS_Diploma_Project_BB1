from src.web_scraper import Scraper
from src.csv_class import CSVSaver
from loguru import logger

def scrapnwrite():
    """ Функция вызова сервиса веб-скрапинга и записи в данных в файл CSV"""
    logger.add("launch_info.log", rotation="1 MB", level="INFO", backtrace=True, diagnose=True)
    site = 'https://goldapple.ru/parfjumerija'
    scraper = Scraper(site, 1)
    scraper.scrape()
    data = scraper.get_data()

    logger.info(data)
    logger.info(f'Заполнено позиций link: {len(data['link'])}')
    logger.info(f'Заполнено позиций name: {len(data['name'])}')
    logger.info(f'Заполнено позиций price: {len(data['price'])}')
    logger.info(f'Заполнено позиций rating: {len(data['rating'])}')
    logger.info(f'Заполнено позиций description: {len(data['description'])}')
    logger.info(f'Заполнено позиций manual: {len(data['manual'])}')
    logger.info(f'Заполнено позиций country: {len(data['country'])}')

    csv_saver = CSVSaver()
    csv_saver.write_data(data)

def waste_csv():
    """ Функция удаления данных из файла CSV"""
    csv_saver = CSVSaver()
    csv_saver.del_data()
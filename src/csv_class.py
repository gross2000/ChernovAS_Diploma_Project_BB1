# Функционал выгрузки полученных результатов в CSV
import pandas as pd
from src.web_scraper import Scraper


site = "https://goldapple.ru/parfjumerija"

scraper = Scraper(site, 1)
scraper.scrape()
data = scraper.get_data()

# Создание DataFrame из данных
df = pd.DataFrame(data)

#Сохранение DataFrame в CSV-файл
df.to_csv('results.csv', index=False)
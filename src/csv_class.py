"""Функционал выгрузки полученных результатов в CSV"""
from abc import ABC, abstractmethod
import pandas as pd


class Filesaver(ABC):

    def __init__(self, filename):
        self.filename = filename

    @abstractmethod
    def write_data(self, data):
        pass

    @abstractmethod
    def del_data(self):
        pass


class CSVSaver(Filesaver):
    """"Класс для записи в csv-файл"""

    def __init__(self, filename = 'results.csv'):
        super().__init__(filename)


    def write_data(self, data):
        """ Запись данных в csv """
        df = pd.DataFrame(data)
        df.to_csv(self.filename, index = False)


    def del_data(self):
        """ Удаление данных из файла """
        with open(self.filename, 'w') as f:
            f.truncate(0)
"""Тестовая часть для функционала сохранения данных в CSV"""
import os
import pytest
import pandas as pd
from src.csv_class import CSVSaver

@pytest.fixture
def csv_saver(tmp_path):
    """ Фикстура для создания экземпляра CSVSaver и временного файла """
    filename = os.path.join(os.path.dirname(__file__), '..', 'test.csv')
    saver = CSVSaver(filename)
    return saver

def test_write_data(csv_saver):
    """ Тест для записи данных в csv файл """
    data = {'column1': [1, 2, 3], 'column2': [4, 5, 6]}
    csv_saver.write_data(data)

    # Проверяем, что файл создан и содержит данные
    df = pd.read_csv(csv_saver.filename)
    assert not df.empty
    assert set(df.columns) == {'column1', 'column2'}
    assert df.shape[0] == 3  # Проверяем количество записей
    assert df.shape[1] == 2  # Проверяем количество колонок

def test_del_data(csv_saver):
    """ Тест для удаления данных из csv файла """
    data = {'column1': [1, 2, 3], 'column2': [4, 5, 6]}
    csv_saver.write_data(data)

    # Удаляем данные
    csv_saver.del_data()

    # Проверяем, существует ли файл и пуст ли он
    assert os.path.exists(csv_saver.filename)
    assert os.path.getsize(csv_saver.filename) == 0, "Файл test.csv не пустой"


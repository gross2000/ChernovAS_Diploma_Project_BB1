Структура проекта:
1. Основная логика программы расположена в каталге Project/src/.
2. Файл web_scraper.py содержит класс Scraper для выполнения основного функцилнала по web-скрапингу сайта с использованием объектно-ориентированного подхода, а также применением регулярных выражений (regex).
3. Файл csv_class.py содержит функционал записи (удаления) результатов сбора и обработки данных, полученных с сайта в формате CSV (см. файл Project/results.csv).
4. В файле utils.py представлена логика вызовов классов и методов основного функционала.
5. В каталоге Project/tests/ вынесена тестовая часть, для кода файлов web_scraper.py и csv_class.py соответственно. Тесты запускаются из команной, результаты записываются в файл .coverege.
6. В файл main.py (корень проекта) вынесены команды для запуска проекта.
7. В проекте реализовно логирование процесса веб-скрапинга. Запись производится в соответствующие файлы .log.
8. Кроме того, в корне проекта представлены файлы:
   results.csv (результаты веб-скрапинга);
   requirements.txt (окружение);
   test.csv (файл для тестирования функционала записи в CSV-формат).

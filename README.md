# 28.1-Autotest_Rostelecom
Дипломная работа

Автоматизированное тестирование веб-интерфейса сайта Ростелеком https://b2c.passport.rt.ru/ 

В файле base.py содержится шаблон PageObject для Python.

В файле elements.py содержится вспомогательный класс для определения веб-элементов.

В файле registration_page.py содержится класс страницы регистрации на сайте Ростелеком.

В файле auth_page.py содержится класс страницы подтверждения регистрации.

В файле test_rostelecom.py располагается набор тестов для веб-интерфейса сайта.

В файле conftest.py находятся фикстуры по дополнительным настройкам.

ИНСТРУКЦИЯ ПО ЗАПУСКУ:

Скачать драйвер для используемого браузера, в текущей работе использовался Google Chrome - https://chromedriver.chromium.org/downloads

Установить все требуемые библиотеки из файла requirements.txt:

pip install -r requirements.txt

Запустить разработанные тесты с помощью команды:

python -m pytest -v --driver Chrome --driver-path C:/Documents/chromedriver.exe tests/test_rostelecom.py

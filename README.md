# LH2

# Инструкция по запуску проекта

## Шаг 1: Клонирование репозитория
- git clone <URL_вашего_репозитория>
- cd archive_tester

## Шаг 2: Создание виртуального окружения
- python3 -m venv venv
- source venv/bin/activate

## Шаг 3: Установка зависимостей
- pip install -r requirements.txt

## Шаг 4: Установка необходимого пакета для CRC32
- sudo apt update
- sudo apt install libarchive-zip-perl

## Шаг 5: Подготовка тестовой среды
- Создайте необходимые директории
- Создайте исходные файлы

## Шаг 6: Запуск тестов
### Позитивные тесты
- pytest -v test_archive.py

### Негативные тесты
- pytest -v test_negative_archive.py

### Запуск всех тестов
- pytest -v

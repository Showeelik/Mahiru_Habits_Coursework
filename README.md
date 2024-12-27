# Mahiru Habits - Трекер полезных привычек

## Описание проекта

Проект представляет собой REST API сервис для отслеживания полезных привычек. Пользователи могут создавать, отслеживать и делиться своими привычками, получать уведомления через Telegram.

## Функциональность

- Регистрация и авторизация пользователей
- CRUD операции с привычками
- Публичные и приватные привычки
- Интеграция с Telegram для уведомлений
- Отложенные задачи через Celery
- Валидация данных привычек
- Пагинация (5 привычек на страницу)
- API документация (Swagger/ReDoc)

## Технологии

- Python 3.10+
- Django 5.1
- Django REST Framework
- PostgreSQL
- Celery
- Redis
- Simple JWT
- Swagger/drf-yasg

## Установка и запуск

### Предварительные требования

- Python 3.10+
- PostgreSQL
- Redis

### Установка

1. Клонировать репозиторий:
    ```bash
    git clone https://github.com/Showeelik/Mahiru_Habits_Coursework.git
    ```
2. Установить Poetry:
    ```bash
    pip install poetry
    ```
3. Установить зависимости и создать виртуальное окружение:
    ```bash
    poetry install
    ```
4. Активировать виртуальное окружение:
    ```bash
    poetry shell
    ```
4. Создать файл `.env` на основе `.env_template` и заполнить необходимые переменные окружения.

5. Выполнить миграции:
    ```bash
    python manage.py migrate
    ```

### Установка Redis

1. Установите Redis:
   - На macOS: используйте Homebrew
     ```sh
     brew install redis
     ```
   - На Ubuntu/Debian:
     ```sh
     sudo apt update
     sudo apt install redis-server
     ```
   - На Windows: скачайте и установите Redis с официального сайта или используйте WSL (Windows Subsystem for Linux).

2. Запустите Redis сервер:
   - На macOS и Linux:
     ```sh
     redis-server
     ```
   - На Windows:
     Запустите `redis-server.exe` из установленной директории.

3. Проверьте, что Redis сервер запущен:
   - Выполните команду:
     ```sh
     redis-cli ping
     ```
   - Если сервер работает, вы получите ответ `PONG`.

4. Настройте Redis сервер (опционально):
   - Откройте файл конфигурации `redis.conf` и внесите необходимые изменения.

### Запуск

1. Запустить Redis сервер.

2. Запустить Celery:
    ```bash
    celery -A проект worker -l info
    ```
3. Запустить Django сервер:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

- `POST /api/register/` - Регистрация пользователя
- `POST /api/token/` - Получение JWT токена
- `GET /api/habits/` - Список привычек авторизованного пользователя
- `POST /api/habits/` - Создание новой привычки
- `GET /api/habits/public/` - Список публичных привычек
- `GET /api/habits/<int:pk>/` - Получение деталей конкретной привычки
- `PUT /api/habits/<int:pk>/` - Обновление конкретной привычки
- `PATCH /api/habits/<int:pk>/` - Частичное обновление конкретной привычки
- `DELETE /api/habits/<int:pk>/` - Удаление конкретной привычки
- `/swagger/` - Swagger документация
- `/redoc/` - ReDoc документация

## Тестирование

Инструкции по тестированию проекта.


## Автор

[mahiru]

## Контакты

Email: [mahiru@mahiru.com]  
Telegram: [@mahiru]

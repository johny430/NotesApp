Инструкция по запуску FastAPI-сервера и Telegram-бота
1. Установка Docker
Установите Docker: Docker Installation Guide

Проверьте установку:

bash
Копировать код
docker --version
2. Клонирование репозитория
Клонируйте проект:

bash
Копировать код
git clone <URL репозитория>
cd <название директории проекта>
3. Настройка сервера (FastAPI)
Создайте файл .env в папке server/:

bash
Копировать код
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
Соберите и запустите Docker-контейнер сервера:

bash
Копировать код
cd server/
docker build -t fastapi-app .
docker run -d -p 8000:8000 fastapi-app
Теперь сервер доступен по адресу http://127.0.0.1:8000.

4. Настройка Telegram-бота
Получите токен у @BotFather и добавьте его в файл .env в папке bot/:

bash
Копировать код
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
Установите зависимости и запустите бота:

bash
Копировать код
cd bot/
pip install -r requirements_bot.txt
python bot.py
5. Команды бота
/auth — авторизация.
/notes — просмотр заметок.
/new_note — создание заметки.
/search_notes — поиск заметок по тегам.
6. Остановка контейнеров
Остановите и удалите контейнеры сервера:

bash
Копировать код
docker ps  # список запущенных контейнеров
docker stop <container_id>
docker rm <container_id>
7. База данных
Для локального запуска PostgreSQL можно использовать Docker:

bash
Копировать код
docker run --name postgres -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres

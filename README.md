Инструкция по запуску FastAPI-сервера и Telegram-бота    
1. Клонирование репозитория  
Клонируйте проект:  
git clone https://github.com/johny430/NotesApp
cd NotesApp
3. Настройка сервера (FastAPI)  
Создайте файл .env в папке server/:  
  
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname   
SECRET_KEY=your_secret_key  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=30  
Соберите и запустите Docker-контейнер сервера:  
cd server/  
docker build -t fastapi-app .  
docker run -d -p 8000:8000 fastapi-app  

4. Настройка Telegram-бота  
Получите токен у @BotFather и добавьте его в файл .env в папке bot.
TELEGRAM_BOT_TOKEN=your_telegram_bot_token  
Установите зависимости и запустите бота:  
cd bot/  
pip install -r requirements_bot.txt  
python bot.py  
5. Команды бота  
/auth — авторизация.  
/notes — просмотр заметок.  
/new_note — создание заметки.  
/search_notes — поиск заметок по тегам.  
7. База данных  
Для локального запуска PostgreSQL можно использовать Docker:  
  
docker run --name postgres -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres  

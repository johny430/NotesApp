import logging
import os

import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from dotenv import load_dotenv

API_URL = "http://127.0.0.1:8000"

load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

authorized_users = {}


# Обработчик команды /auth для авторизации пользователя через Telegram
@dp.message(Command("auth"))
async def auth_user(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    username = message.from_user.username

    response = requests.post(f"{API_URL}/register", json={"username": username, "password": "telegram_pass"})

    if response.status_code == 200:
        token_response = requests.post(f"{API_URL}/token", data={"username": username, "password": "telegram_pass"})
        if token_response.status_code == 200:
            token = token_response.json()["access_token"]
            authorized_users[chat_id] = token
            await message.answer(f"Вы успешно авторизованы, {username}!")
        else:
            await message.answer("Ошибка при получении токена.")
    else:
        await message.answer("Ошибка при регистрации пользователя.")


# Обработчик команды /notes для получения списка заметок
@dp.message(Command("notes"))
async def get_notes(message: Message):
    chat_id = message.from_user.id
    token = authorized_users.get(chat_id)

    if not token:
        await message.answer("Сначала авторизуйтесь с помощью команды /auth")
        return

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/notes", headers=headers)

    if response.status_code == 200:
        notes = response.json()
        if notes:
            reply = "\n\n".join([f"Заголовок: {note['title']}\nСодержание: {note['content']}" for note in notes])
        else:
            reply = "У вас пока нет заметок."
        await message.answer(reply)
    else:
        await message.answer("Ошибка при получении заметок.")


# Обработчик команды /new_note для создания новой заметки
@dp.message(Command("new_note"))
async def create_note(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    token = authorized_users.get(chat_id)

    if not token:
        await message.answer("Сначала авторизуйтесь с помощью команды /auth")
        return

    await message.answer("Введите заголовок заметки:")
    await state.set_state("awaiting_title")


# Обработчик для получения заголовка заметки
@dp.message(F.state == "awaiting_title")
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите содержание заметки:")
    await state.set_state("awaiting_content")


# Обработчик для получения содержания заметки и создания заметки
@dp.message(F.state == "awaiting_content")
async def process_content(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    token = authorized_users.get(chat_id)

    data = await state.get_data()
    title = data['title']
    content = message.text

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{API_URL}/notes", headers=headers, json={"title": title, "content": content})

    if response.status_code == 200:
        await message.answer("Заметка успешно создана!")
    else:
        await message.answer("Ошибка при создании заметки.")

    await state.clear()


# Обработчик команды /search_notes для поиска заметок по тегам
@dp.message(Command("search_notes"))
async def search_notes(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    token = authorized_users.get(chat_id)

    if not token:
        await message.answer("Сначала авторизуйтесь с помощью команды /auth")
        return

    await message.answer("Введите теги для поиска (через запятую):")
    await state.set_state("awaiting_tags")


# Обработчик для получения тегов и поиска заметок
@dp.message(F.state == "awaiting_tags")
async def process_tags(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    token = authorized_users.get(chat_id)
    tags = message.text.split(',')
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/notes", headers=headers, params={"tags": tags})

    if response.status_code == 200:
        notes = response.json()
        if notes:
            reply = "\n\n".join([f"Заголовок: {note['title']}\nСодержание: {note['content']}" for note in notes])
        else:
            reply = "Заметки с такими тегами не найдены."
        await message.answer(reply)
    else:
        await message.answer("Ошибка при поиске заметок.")
    await state.clear()


# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)

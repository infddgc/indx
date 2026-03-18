import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ChatAction
import os

TOKEN = os.getenv("8761314650:AAH3nnM5auKtGod8KS1Asv2Kotx-qUOwTbQ")
TOGETHER_API_KEY = os.getenv("key_CZAeBCn6UyinngcrFKCav")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ⚡️ ПАМЯТЬ В RAM (СУПЕР БЫСТРО)
memory = {}

MAX_HISTORY = 4  # минимум = максимум скорости

# ⚡️ AI
def ask_ai(messages):
    try:
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                # ⚡️ БЫСТРАЯ МОДЕЛЬ
                "model": "mistralai/Mistral-7B-Instruct-v0.1",
                "messages": messages,
                "max_tokens": 150,   # меньше = быстрее
                "temperature": 0.6
            },
            timeout=6  # ⚡️ очень быстрый таймаут
        )

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except:
        return "⚠️ Ошибка, попробуй ещё раз"

# ⚡️ ЧАТ
@dp.message()
async def chat(message: Message):
    user_id = message.from_user.id

    # создаём память
    if user_id not in memory:
        memory[user_id] = []

    # добавляем сообщение
    memory[user_id].append({
        "role": "user",
        "content": message.text[:300]  # обрезаем
    })

    # ограничиваем память
    memory[user_id] = memory[user_id][-MAX_HISTORY:]

    # ⚡️ моментальный typing
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    # ⚡️ быстрый запрос
    reply = ask_ai([
        {"role": "system", "content": "Отвечай коротко и быстро на русском"}
    ] + memory[user_id])

    # сохраняем ответ
    memory[user_id].append({
        "role": "assistant",
        "content": reply
    })

    await message.answer(reply)

# 🚀 запуск
async def main():
    print("ULTRA FAST BOT ⚡️ запущен")
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
import asyncio
import aiohttp
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

TOKEN = os.getenv("BOT_TOKEN")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ⚡ ПАМЯТЬ
memory = {}
MAX_HISTORY = 5

# ⚡ AI запрос (БЫСТРЫЙ)
async def ask_ai(messages):
    url = "https://api.together.xyz/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as resp:
            result = await resp.json()
            return result["choices"][0]["message"]["content"]

# 🧹 Очистка памяти
@dp.message(F.text == "/clear")
async def clear(message: Message):
    memory[message.chat.id] = []
    await message.answer("🧹 Память очищена!")

# 🤖 Основной чат
@dp.message()
async def chat(message: Message):
    user_id = message.chat.id

    if user_id not in memory:
        memory[user_id] = []

    memory[user_id].append({"role": "user", "content": message.text})
    memory[user_id] = memory[user_id][-MAX_HISTORY:]

    try:
        await bot.send_chat_action(message.chat.id, "typing")

        reply = await ask_ai(memory[user_id])

        memory[user_id].append({"role": "assistant", "content": reply})

        await message.answer(reply)

    except Exception as e:
        await message.answer("❌ Ошибка, попробуй позже")
        print(e)

# 🚀 ЗАПУСК
async def main():
    print("⚡ ULTRA FAST BOT запущен")
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())

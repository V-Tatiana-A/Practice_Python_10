from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage



bot= Bot(token='5925560522:AAGfTgxXf023wLDQJxE0NWitehFY1E3sAIQ')
storage = MemoryStorage()
dp=Dispatcher(bot, storage=storage)

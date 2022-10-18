from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# AnkiAssistantBot
TOKEN = "5494354739:AAHFcZju_F-v3t7BS9CirBrmT4kV89Zjs1o"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

id_creator = 1068817703
id_andry_straj = 1699996923


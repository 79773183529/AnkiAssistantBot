import asyncio
import logging

import emoji
from aiogram import Bot
from aiogram.types import BotCommand
from common import register_handlers_common
from add_cards import register_handlers_topic
from play import register_handlers_play
from contact import register_handlers_contact
from helper import register_handlers_helper

from bot import bot, dp

logging.basicConfig(level=logging.INFO)


async def main():
    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_handlers_topic(dp)
    register_handlers_play(dp)
    register_handlers_contact(dp)
    register_handlers_helper(dp)



    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/add_cards", description=f"{emoji.emojize(':memo:')} Добавить карточки"),
        BotCommand(command="/play", description=f"{emoji.emojize(':magnifying_glass_tilted_left:')} Играть"
                   ),
        BotCommand(command="/delete", description=f"{emoji.emojize(':wastebasket:')}Удалить карточки"),
        BotCommand(command="/cancel", description=f"{emoji.emojize(':chequered_flag:')} Выход"),
        BotCommand(command="/contact", description=f"{emoji.emojize(':tongue:')}Связаться с разработчиками"),
        BotCommand(command="/help", description=f"{emoji.emojize(':tongue:')}Получить помощь"),
    ]
    await bot.set_my_commands(commands)


if __name__ == '__main__':
    asyncio.run(main())

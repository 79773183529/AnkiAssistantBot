import emoji
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType

from bot import bot, id_creator
from add_cards import user_markup_exit


class OrderContact(StatesGroup):
    waiting_for_message = State()


async def cmd_contact(message: types.Message):
    await message.answer(emoji.emojize(":woman_office_worker:"))
    await message.answer(
        'Сейчас вы можете отправить мне сообщение, которое я перешлю разработчикам или нажмите'
        ' <b>/cancel</b> для выхода',
        parse_mode=types.ParseMode.HTML,
        reply_markup=user_markup_exit)
    await OrderContact.waiting_for_message.set()


async def cmd_message(message: types.Message, state: FSMContext):
    await message.answer(
        ' Ваше сообщение отправлено',
        parse_mode=types.ParseMode.HTML,
        )
    await bot.send_message(id_creator,
                           f'Bot: AnkiAssistantBot \n'
                           f'ID: {message.from_user.id}\n'
                           f'name: {message.from_user.first_name}\n'
                           f'text: {message.text}\n'
                           )
    await bot.send_message(id_creator,
                           message)
    await state.finish()


def register_handlers_contact(dp: Dispatcher):
    dp.register_message_handler(cmd_contact, commands="contact", state="*")
    dp.register_message_handler(cmd_message,
                                content_types=[ContentType.VOICE, ContentType.TEXT, ContentType.DOCUMENT],
                                state=OrderContact.waiting_for_message)

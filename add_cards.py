import asyncio
import emoji

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType
from aiogram.utils.callback_data import CallbackData

from bot import bot, TOKEN

from with_files import get_list_topic, get_user_topic, add_user_topic, get_name

cb = CallbackData("call", "group", "id", "topic_number")


class OrderTopic(StatesGroup):
    waiting_for_topic_name = State()


# Выводит на экран Inline клавиатуру с вариантами
async def topic_start(message: types.Message):
    list_topic = get_list_topic()
    markup = types.InlineKeyboardMarkup()
    button = []
    for i in range(len(list_topic)):
        button.append(types.InlineKeyboardButton(text=f'Добавить "{list_topic[i][2]}"',
                                                 callback_data=cb.new(group='topic',
                                                                      id=message.from_user.id,
                                                                      topic_number=list_topic[i][1])
                                                 ))
        markup.row(button[i])

    await message.answer(f'Выберите нужную  главу ', reply_markup=markup)
    await message.answer('..', reply_markup=user_markup_exit)
    await OrderTopic.waiting_for_topic_name.set()


# Обрабатывает коллбеки. Принимает номер главы
async def set_topic(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    number_topic = callback_data["topic_number"]
    user_id = callback_data["id"]
    if number_topic not in get_user_topic(user_id):
        await bot.send_message(user_id, emoji.emojize(":woman_technologist:"))  # ":woman_office_worker:"
        add_user_topic(user_id, number_topic)
        await bot.send_message(user_id, 'Отлично. Я добавила карточки в вашу колоду')
        await asyncio.sleep(1)
        await bot.send_message(user_id, 'Что бы воспользоваться ими войдите в меню и нажмите '
                                        '<i><b>play</b></i>',
                               parse_mode=types.ParseMode.HTML)
        await call.answer()
        await state.finish()
    else:
        await bot.send_message(user_id, emoji.emojize(":woman_shrugging:"))
        await bot.send_message(user_id, get_name(user_id))
        await bot.send_message(user_id, 'Эта глава уже есть в вашем списке')
        await asyncio.sleep(3)
        await bot.send_message(user_id, 'Попробуйте выбрать другую главу или нажмите \n'
                                        '<i><b>cancel</b></i>\n'
                                        'для выхода',
                               parse_mode=types.ParseMode.HTML,
                               reply_markup=user_markup_exit)
        await call.answer()


def register_handlers_topic(dp: Dispatcher):
    dp.register_message_handler(topic_start, commands="add_cards", state="*")
    dp.register_callback_query_handler(set_topic,
                                       cb.filter(group=['topic']),
                                       state=OrderTopic.waiting_for_topic_name)


user_markup_exit = types.ReplyKeyboardMarkup(resize_keyboard=True)
user_markup_exit.row('/cancel')

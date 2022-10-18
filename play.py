import asyncio
import emoji

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType, InputFile
from aiogram.utils.callback_data import CallbackData

from bot import bot, TOKEN

from with_files import get_name, get_card_from_stack, return_card_to_stack, return_card_to_file

cb = CallbackData("call", "group", "id", "status")


class OrderPlay(StatesGroup):
    waiting_for_open = State()
    waiting_for_status = State()


# Выводит на экран Inline клавиатуру с вариантами
async def play_start(message: types.Message, state: FSMContext):
    the_card = get_card_from_stack(message.from_user.id).split(';')

    await state.update_data(the_card_list=the_card)

    src_q = the_card[0]

    img = InputFile(src_q)
    await bot.send_photo(message.from_user.id, photo=img)

    markup = types.InlineKeyboardMarkup()
    button_open_answer = types.InlineKeyboardButton("Открыть ответ",
                                                    callback_data=cb.new(group='play',
                                                                         id=message.from_user.id,
                                                                         status='None'))
    markup.row(button_open_answer)
    await message.answer('..', reply_markup=markup)
    await OrderPlay.waiting_for_open.set()


# Обрабатывает коллбеки. Принимает открыть ответ и выводит новую Inline клавиатуру
async def play_answer(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = callback_data["id"]

    user_data = await state.get_data()
    the_card_list = user_data['the_card_list']
    src_a = the_card_list[1]

    markup = types.InlineKeyboardMarkup()
    button = []
    dict_ = {"Не вспомнил или ошибся": "wrong", "С трудом вспомнил": "hard", "Сразу вспомнил": "easy"}
    i = -1
    for key in dict_:
        button.append(types.InlineKeyboardButton(text=key,
                                                 callback_data=cb.new(group='play',
                                                                      id=user_id,
                                                                      status=dict_[key])
                                                 ))
        i += 1
        markup.row(button[i])

    img = InputFile(src_a)
    await bot.send_photo(user_id, photo=img, reply_markup=markup)

    await call.answer()
    await OrderPlay.waiting_for_status.set()


# Обрабатывает коллбеки. Начисляет карточки баллы и записывает в файл
async def play_ball(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = callback_data["id"]
    status = callback_data["status"]

    user_data = await state.get_data()
    the_card_list = user_data['the_card_list']

    name = get_name(user_id)

    await bot.send_message(user_id, emoji.emojize(":woman_technologist:"))

    if status == "wrong":
        await bot.send_message(user_id, f'Бывает {name},\nМы обязательно повторим этот вопрос в ближайшее время')
        the_card_list[2] = '0'
        the_card = ';'.join(the_card_list)
        return_card_to_stack(the_card, user_id)
    elif status == "hard":
        await bot.send_message(user_id, f'Не плохо {name},\nНо мы ещё вернёмся к этому вопрсу')
        the_card = ';'.join(the_card_list)
        return_card_to_stack(the_card, user_id)
    elif status == "easy":
        await bot.send_message(user_id, f'Отлично {name},\nтак держать !!')
        return_card_to_file(the_card_list, user_id)

    await bot.send_message(user_id, 'Нажмите <i><b>/play</b></i> \nчтобы продолжить\n'
                                    'или <i><b>/cancel</b></i> для выхода ',
                           parse_mode=types.ParseMode.HTML,
                           reply_markup=user_markup_exit)

    await call.answer()
    await state.finish()


def register_handlers_play(dp: Dispatcher):
    dp.register_message_handler(play_start, commands="play", state="*")
    dp.register_callback_query_handler(play_answer,
                                       cb.filter(group=['play']),
                                       state=OrderPlay.waiting_for_open)
    dp.register_callback_query_handler(play_ball,
                                       cb.filter(group=['play']),
                                       state=OrderPlay.waiting_for_status)


user_markup_exit = types.ReplyKeyboardMarkup(resize_keyboard=True)
user_markup_exit.row('/cancel')

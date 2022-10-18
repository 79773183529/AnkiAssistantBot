import emoji
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import asyncio

from add_cards import user_markup_exit
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData

from bot import bot

cb = CallbackData("call", "group", "id", "name")


class OrderHelp(StatesGroup):
    waiting_for_chapter = State()


# Создаём инлайн клавиатуру
async def help_start(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    button = []
    button_help_search = types.InlineKeyboardButton('Как начать обучение',
                                                    callback_data=cb.new(group='help',
                                                                         id=message.from_user.id,
                                                                         name='start'))
    markup.row(button_help_search)

    button_help_contact = types.InlineKeyboardButton('Как связаться с разработчиком',
                                                     callback_data=cb.new(group='help',
                                                                          id=message.from_user.id,
                                                                          name='contact'))
    markup.row(button_help_contact)

    button_help_help = types.InlineKeyboardButton('Как получить помощь',
                                                  callback_data=cb.new(group='help',
                                                                       id=message.from_user.id,
                                                                       name='help'))
    markup.row(button_help_help)

    await message.answer(emoji.emojize(":woman_office_worker:"))
    await message.answer('В чём я могу вам помочь ?', reply_markup=markup)
    await message.answer('..', reply_markup=user_markup_exit)
    await OrderHelp.waiting_for_chapter.set()


async def set_help(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data["name"] == 'start':
        await bot.send_message(callback_data["id"], emoji.emojize(":woman_technologist:"))
        await bot.send_message(callback_data["id"],
                               'Для того чтобы начать пользоваться ботом\n'
                               'войдите в меню\n'
                               'нажмите <b><i>добавить карточки</i></b>\n'
                               'из предложенных вариантов выберите только те главы, которые уже полностью успели '
                               'изучить\n'
                               'Далее снова войдите в меню\n'
                               'и нажмите <b><i>играть</i></b>\n'
                               'Вам будет отправлена карточка с вопросом\n'
                               'Прочитав вопрос и вспомнив ответ\n'
                               'Нажмите <b><i>открыть ответ</i></b>\n'
                               'В резульате этого вам придёт карточка с ответом\n'
                               'Внимательно прочитайте правильный ответ и максимально честно оцените свой с помощью '
                               'появившихся кнопок с вариантами.\n'
                               'Для продолжения снова нажмите <b><i>играть</i></b>',
                               parse_mode=types.ParseMode.HTML,
                               )

    elif callback_data["name"] == 'contact':
        await bot.send_message(callback_data["id"], emoji.emojize(":woman_technologist:"))
        await bot.send_message(callback_data["id"],
                               'Уже задумали что-нибудь нажаловаться на меня ??\n\n'
                               '<i>Признаться я от вас такого не ожидала :))</i>',
                               parse_mode=types.ParseMode.HTML)
        await asyncio.sleep(4)
        await bot.send_message(callback_data["id"],
                               'Для того чтобы отправить сообщение разработчикам - просто зайдите в меню и нажмите\n'
                               '<b>/contact</b>',
                               parse_mode=types.ParseMode.HTML,
                               )

    elif callback_data["name"] == 'help':
        await bot.send_message(callback_data["id"], emoji.emojize(":woman_facepalming:"))
        await bot.send_message(callback_data["id"],
                               'Для того чтобы получить инструкции просто войдите в '
                               ' меню и нажмите\n <b>/help</b>. \n'
                               'После чего выберите интиресующий вас раздел',
                               parse_mode=types.ParseMode.HTML,
                               )
    await call.answer()
    await state.finish()


def register_handlers_helper(dp: Dispatcher):
    dp.register_message_handler(help_start, commands="help", state="*")
    dp.register_callback_query_handler(set_help,
                                       cb.filter(group=['help']),
                                       state=OrderHelp.waiting_for_chapter)

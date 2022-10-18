import emoji
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from with_files import start_registration


class OrderGreeting(StatesGroup):
    waiting_for_user_name = State()


async def cmd_start(message: types.Message, state: FSMContext):

    await message.answer('Привет, Я AnkiAssistant !!!')

    await message.answer(emoji.emojize(":woman_raising_hand:"))
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["/меню", "/помощь"]
    keyboard.add(*buttons)
    await message.answer(
        '\n\n И я совершенно\n<b>бесплатно</b> и \n'
        '<b>без регистрации</b> \nпомогу вам легко и эффективно повторить материал пройденный'
        ' на курсе  "Поколение Python": курс для профессионалов от "Beegeek" \n\n'
        '<i> А как я могу к вам обращаться ??  Пришлите мне своё имя </i>',
        parse_mode=types.ParseMode.HTML,
    )
    await OrderGreeting.waiting_for_user_name.set()


async def get_user_name(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    name = message.text
    start_registration(message, name)

    await message.answer(f'Рада знакомству {name}', reply_markup=keyboard)
    await message.answer("Для того чтобы приступить к работе войдите в <i><b>menu</b></i> и выберите"
                         " 'добавить карточки'",
                         parse_mode=types.ParseMode.HTML)
    await state.finish()


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено")
    await message.answer(emoji.emojize(":woman_frowning:"))


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(get_user_name, state=OrderGreeting.waiting_for_user_name)
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")

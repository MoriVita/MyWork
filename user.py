from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery #InlineKeyboardMarkup, InlineKeyboardButton,
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from data import month, data_us, users_data
from state import Reg

user_router = Router()



async def kb_next():
    nb = InlineKeyboardBuilder()
    nb.button(
        text='начать', callback_data= "next"
    )
    return nb.as_markup()



async def kb_month():
    kb = InlineKeyboardBuilder()
    for month_number, (name, days) in month.items():
        kb.button(
            text=name,
            callback_data=f"month_{month_number}"
        )
    return kb.adjust(4).as_markup()


async def kb_data_us():
    kb_us = InlineKeyboardBuilder()
    for data_u in data_us:
        kb_us.button(
            text = data_u,
            callback_data=f"data_{data_u}"
        )
    return kb_us.adjust(2).as_markup()


async def kb_mn():
    kb_mns = InlineKeyboardBuilder()
    kb_mns.button(
        text="продолжить",
        callback_data = "menu"
    )
    return kb_mns.as_markup()

async def add_expenses(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id


    if user_id not in users_data:
        users_data[user_id] = {
            "categories": {},
            "expenses": []
        }
    await state.set_state(Reg.category)
    await callback.message.answer(
        "выберите категорию либо введите новую",
     )
    print(users_data)

####################################################################################################################################

# @user_router.callback_query(F.data == str(month["ноябрь"]))
# async def kb_optional(callback: CallbackQuery, state: FSMContext):
#     await state.set_state(Reg.day)
#     await callback.message.answer('введите день')
#
#     await callback.answer()


####доделать сравнение
@user_router.message(Reg.day)
async def handle_day(message: Message, state: FSMContext):

    await state.update_data(us_day=message.text)  # сохраняем день
    day = int(message.text)
    data = await state.get_data()
    if day > 50:
        await message.answer("много")
    print(data)
    month_name = data.get("month_name")

    await message.answer(
        f"Текущий месяц: {month_name},\n день: {message.text}",
        reply_markup = await kb_mn()
    )
    await state.clear()  # можно очистить состояние


@user_router.callback_query(F.data.startswith("data_"))
async def handle_data(callback: CallbackQuery, state: FSMContext):
    action = callback.data.replace("data_", "")
    if action == data_us[0]:
        await add_expenses(callback, state)



@user_router.callback_query(F.data.startswith("month_"))
async def handle_month(callback: CallbackQuery, state: FSMContext):
        value = int(callback.data.split("_")[1])
        # value = callback.data.split("_")[1]
        # month_name = [k for k, v in month.items() if str(v) == value][0]

        name, days = month[value]

        await state.update_data(
            month=value,
            month_name=name,
            days=days
        )
        await state.set_state(Reg.day)
        await callback.message.answer("Введите день")
        await callback.answer()


        # month_name = next(k for k, v in month.items() if str(v) == value)
        # await state.update_data(month=value, month_name=month_name)

        # data = await state.get_data()
        # selected_month = data.get("month")
        #
        # text = "\n".join(f"{k}: {v}" for k,v in month.items())

        # if value == str(month["ноябрь"]):




@user_router.callback_query(F.data == 'next')
async def cb_next(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Reg.month)  # устанавливаем состояние
    await callback.message.answer(
        'выберите текущий месяц из списка',
        reply_markup=await kb_month()
    )



@user_router.callback_query(F.data == 'menu')
async def cb_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        'выберите действие',
        reply_markup=await kb_data_us()
    )



##################################################################
@user_router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('text', reply_markup= await kb_next())







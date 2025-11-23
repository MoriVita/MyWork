from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from data import month
from state import Reg

user_router = Router()



async def kb_next():
    nb = InlineKeyboardBuilder()
    nb.button(
        text='начать', callback_data= "next"
    )
    return nb.adjust(2).as_markup()



async def kb_month():
    kb = InlineKeyboardBuilder()
    for month_name, month_number in month.items():
        kb.button(
            text=month_name,
            callback_data=f"month_{month_number}"
        )
    return kb.adjust(2).as_markup()


async def kb_optional():
    rb = InlineKeyboardBuilder()
    rb.button(
        text = 'новая кнопка', callback_data = 'next'
    )
    return rb.adjust(2).as_markup()


####################################################################################################################################
@user_router.callback_query(F.data.startswith("month_"))
async def handle_month(callback: CallbackQuery, state: FSMContext):
        value = callback.data.split("_")[1]

        await state.update_data(month=callback.data)
        data = await state.get_data()

        text = "\n".join(f"{k}: {v}" for k,v in month.items())

        if value == str(month["ноябрь"]):
            await callback.message.answer(text, reply_markup = await kb_optional())





@user_router.callback_query(F.data == 'next')
async def cb_next(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Reg.month)  # устанавливаем состояние
    await callback.message.answer(
        'выберите текущий месяц из списка',
        reply_markup=await kb_month()
    )



# @user_router.callback_query(Reg.month)
# async def cb_month(callback: CallbackQuery, state: FSMContext):
#     await state.update_data(month=callback.data)
#     data = await state.get_data()
#     print(data)
#     # можно отправить подтверждение
#     await callback.message.answer(f"Вы выбрали: {data}")
#     await callback.answer()  # закрываем "часики" на кнопке







##################################################################

@user_router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('text', reply_markup= await kb_next())







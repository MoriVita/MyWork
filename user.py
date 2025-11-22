from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from state import Reg

user_router = Router()


async def kb_next():
    nb = InlineKeyboardBuilder()
    nb.button(
        text='начать', callback_data= "next"
    )
    return nb.adjust(2).as_markup()

# async def kb_month():
#     kb = InlineKeyboardBuilder()
#     kb.button(
#         text='input month', callback_data= "month"
#     )

####################################################################################################################################


@user_router.callback_query(F.data == 'next')
async def cb_next(callback: CallbackQuery):
    await callback.message.answer('n_text')




##################################################################

@user_router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('text', reply_markup= await kb_next())







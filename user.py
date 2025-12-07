from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery #InlineKeyboardMarkup, InlineKeyboardButton,
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

from data import month, data_us, users_data
from state import Reg

user_router = Router()

#test

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
        reply_markup=await kb_categories(user_id)
     )
    # await state.update_data(categories = callback.message.text)
    # print(users_data)



@user_router.message(Reg.category)
async def new_category(message: Message, state: FSMContext):
    user_id = message.from_user.id
    category = message.text

    if user_id not in users_data:
        users_data[user_id] = {
            "categories": {},
            "expenses": []
        }

    users_data[user_id]["categories"][category] = {"types": []}

    await message.answer(
        f"Категория '{category}' добавлена.",
        reply_markup=await kb_categories(user_id)
    )
    await state.clear()



@user_router.message(Reg.type)
async def reg_type(message: Message, state: FSMContext):
    user_id = message.from_user.id
    expense_type = message.text
    data = await state.get_data()
    category = data.get("category")

    if user_id not in users_data:
        users_data[user_id] = {
            "categories": {},
            "expenses": []
        }

    if category and category in users_data[user_id]["categories"]:
        # Добавляем тип в список типов категории, если его еще нет
        if expense_type not in users_data[user_id]["categories"][category]["types"]:
            users_data[user_id]["categories"][category]["types"].append(expense_type)
        
        await state.update_data(type=expense_type)
        await message.answer(
            f"Тип расхода '{expense_type}' добавлен. Введите сумму:"
        )
        await state.set_state(Reg.amount)
    else:
        await message.answer("Ошибка: категория не найдена. Начните заново.")
        await state.clear()


async def kb_categories(user_id):
    kb = InlineKeyboardBuilder()
    
    if user_id not in users_data:
        users_data[user_id] = {
            "categories": {},
            "expenses": []
        }
    
    categories = users_data[user_id]["categories"]

    for cat in categories.keys():
        kb.button(
            text=cat,
            callback_data=f"cat_{cat}"
        )
    kb.button(
        text="Добавить новую категорию:",
        callback_data = "new_category"
    )
    return kb.adjust(2).as_markup()


async def kb_types(user_id, category):
    kb_types = InlineKeyboardBuilder()
    
  
    if user_id not in users_data:
        users_data[user_id] = {
            "categories": {},
            "expenses": []
        }
    
    if category not in users_data[user_id]["categories"]:
        users_data[user_id]["categories"][category] = {"types": []}
    
    types = users_data[user_id]["categories"][category]["types"]
    
    for expense_type in types:
        kb_types.button(
            text=expense_type,
            callback_data=f"type_{expense_type}"
        )
    kb_types.button(
        text="Добавить новый тип:",
        callback_data = "new_type"
    )
    return kb_types.adjust(2).as_markup()


####################################################################################################################################



@user_router.callback_query(F.data=="new_category")
async def new_cat(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Reg.category)
    # await state.set_state(Reg.type)
    await callback.message.answer("Введите новую категорию")
    
    await callback.answer()

# @user_router.message(Reg.type)
# async def reg_type(message: Message, state: FSMContext):
#     await state.update_data(type=message.text)



@user_router.callback_query(F.data=="new_type")
async def new_type(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Reg.type)
    await callback.message.answer("ВВедите новый тип расхода")
    await callback.answer()




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
    await state.clear()



@user_router.callback_query(F.data.startswith("cat_"))
async def handle_cat(callback: CallbackQuery, state: FSMContext):
    category = callback.data.replace("cat_", "")
    await state.update_data(category=category)
    await callback.message.answer(
        f"Выбрана категория: {category}, выберите соответствующий тип расхода либо введите новый:",
        reply_markup=await kb_types(callback.from_user.id, category)
    )
    await state.set_state(Reg.type)
    await callback.answer()



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







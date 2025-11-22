import asyncio
from aiogram import Bot, Dispatcher


from user import user_router
from api import TOKEN

dp = Dispatcher()

dp.include_router(user_router)

async def main():
    bot = Bot(token = TOKEN)
    await dp.start_polling(bot)

    # dp = Dispatcher(storage=MemoryStorage())





if __name__ == '__main__':
    asyncio.run(main())

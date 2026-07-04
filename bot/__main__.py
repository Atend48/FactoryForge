import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.data.base_data_base import engine, Base, User, Factory
from bot.handlers.base_commands import base_commands_router
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

dispatcher = Dispatcher()

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    dispatcher.include_router(base_commands_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bots job is finished")
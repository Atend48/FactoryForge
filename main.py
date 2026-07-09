import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.data.models import engine, Base

from bot.handlers.base_commands import base_commands_router
from bot.handlers.improvements_panel import improvements_panel_router
from bot.handlers.manufacture_panel import manufacture_panel_router
from bot.handlers.payments import payment_router
from bot.handlers.statistics_panel import statistic_panel_router
from bot.handlers.worker_panel import worker_panel_router

from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

dispatcher = Dispatcher()

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    dispatcher.include_router(base_commands_router)
    dispatcher.include_router(worker_panel_router)
    dispatcher.include_router(statistic_panel_router)
    dispatcher.include_router(improvements_panel_router)
    dispatcher.include_router(manufacture_panel_router)
    dispatcher.include_router(payment_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
        handlers=[
            logging.FileHandler("bot.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bots job is finished")
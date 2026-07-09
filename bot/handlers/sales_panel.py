from aiogram import Router, F
from aiogram.types import Message

sales_panel_router: Router = Router()

#@sales_panel_router.message(F.text == "💰 Продать")
#async def main_sales_panel(message: Message)
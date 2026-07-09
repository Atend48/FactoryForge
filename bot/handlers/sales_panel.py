from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery

from bot.data.database import get_factory_by_owner, update_factory
from bot.keyboards.inline import sales_kb

sales_panel_router: Router = Router()

@sales_panel_router.message(F.text == "💰 Продать")
async def main_sales_panel(message: Message) -> None:
    factory = await get_factory_by_owner(message.from_user.id)

    if not factory:
        await message.answer(text="❌ У вас еще нет завода! Используйте /start для регистрации.")
        return

    await message.answer_photo(
        photo="https://i.pinimg.com/736x/1f/3e/b0/1f3eb03736fa50975c4ed893c8aaa699.jpg",
        caption=(
            "💰 **Продажа техники** 🪙\n\n"
            f"• Продать всю технику — `{factory.price}/товар` ({factory.price * factory.number_of_production})"
        ), parse_mode=ParseMode.MARKDOWN, reply_markup=sales_kb
    )

@sales_panel_router.callback_query(F.data == "sell_all")
async def sell_all_production(call: CallbackQuery) -> None:
    user_id = call.from_user.id
    factory = await get_factory_by_owner(user_id)

    if not factory:
        await call.answer(text="❌ У вас еще нет завода! Используйте /start для регистрации.", show_alert=True)
        return

    if factory.number_of_production <= 0:
        await call.answer(text="❌ У вас нет продукции на продажу!", show_alert=True)
        return

    updated_factory = await update_factory(user_id=user_id,
                                           number_of_production=0,
                                           moneys=factory.moneys + factory.price * factory.number_of_production)

    await call.answer(
        text=(
            "💰 Вы успешно продали всю технику! 🪙\n"
            f"💵 Денег всего: {updated_factory.moneys}"
        ), show_alert=True
    )
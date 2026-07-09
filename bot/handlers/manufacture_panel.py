from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery

from bot.data.database import get_factory_by_owner, update_factory
from bot.keyboards.inline import manufacture_kb

manufacture_panel_router: Router = Router()

@manufacture_panel_router.message(F.text == "🏭 Производство")
async def manufacture_main_menu(message: Message) -> None:
    factory = await get_factory_by_owner(message.from_user.id)
    await message.answer_photo(
        photo="https://i.pinimg.com/736x/07/4c/98/074c98766a5abb3adf38d69caf03f5b9.jpg",
        caption=(
            f"\t🏭 **Производство** 🧑‍🏭\n\n"
            f"• Произвести одну партию товара — `{factory.production_per_hour}` товара"
        ),
        reply_markup=manufacture_kb,
        parse_mode=ParseMode.MARKDOWN
    )

@manufacture_panel_router.callback_query(F.data == "make_a_batch")
async def make_a_batch(call: CallbackQuery) -> None:
    user_id = call.from_user.id
    factory = await get_factory_by_owner(user_id)

    if not factory:
        await call.answer("❌ У вас еще нет завода! Используйте /start для регистрации.", show_alert=True)
        return

    if factory.worker_fatigue >= 2:
        updated_factory = await update_factory(user_id=user_id,
                                               workers_happiness=factory.workers_happiness - 0.2)
        await call.answer(
            text=(
                 f"🚨 Рабочие слишком устали и отказываются работать! ☹️\n\n"
                 f"😇 Счастье рабочих: {updated_factory.workers_happiness:.1f} (-0.2)\n"
                 f"💤 Отправьте их отдохнуть!"
            ),
            show_alert=True
        )
    else:
        updated_factory = await update_factory(user_id=user_id,
                                               number_of_production=factory.number_of_production + factory.production_per_hour,
                                               worker_fatigue=factory.worker_fatigue + 1)
        await call.answer(
            text=(
                "🏭 Вы произвели новую партию товара! 🧑‍🏭"
                f"🔧 Всего товара: {updated_factory.number_of_production}"
            ),
            show_alert=True
        )
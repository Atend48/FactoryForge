from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery

from bot.data.database import get_factory_by_owner, check_moneys, update_factory
from bot.keyboards.inline import improvements_kb

improvements_panel_router: Router = Router()

UPGRADE_QUALITY_OF_EQUIPMENT: int = 1500
UPGRADE_ENVIRONMENTAL_FRIENDLINESS: int = 2500

@improvements_panel_router.message(F.text == "🔧 Улучшения")
async def main_upgarde(message: Message) -> None:
    await message.answer_photo(
        photo="https://i.pinimg.com/1200x/25/f4/65/25f46539be45cc98c3c927e28ceb629f.jpg",
        caption=(
            f"\t🔧 **Меню улучшений** 🛠️\n\n"
            "• Поднять экологичность — `2,500$` — `+1` к экологочности\n"
            "• Улучшить качество оборудования — `1,500$` — `+1` к качеству оборудования"
        ),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=improvements_kb
    )

@improvements_panel_router.callback_query(F.data.startswith("upgrade_"))
async def upgrade_components(call: CallbackQuery) -> None:
    component: str = call.data.split("_")[-1]
    user_id = call.from_user.id
    factory = await get_factory_by_owner(user_id)

    if not factory:
        await call.answer(text="❌ У вас еще нет завода!", show_alert=True)
        return

    match component:
        case "equipment":
            if factory.moneys >= UPGRADE_QUALITY_OF_EQUIPMENT:
                updated_factory = await update_factory(
                    user_id=user_id,
                    moneys=factory.moneys - UPGRADE_QUALITY_OF_EQUIPMENT,
                    quality_of_equipment=factory.quality_of_equipment + 1
                )
                await call.answer(
                    text=(
                         "✅ Вы успешно улучшили качество оборудования!\n"
                         f"⚙️ Качество техники: {updated_factory.quality_of_equipment}/5\n"
                         f"💵 Денег на счете: {updated_factory.moneys}$"
                    ),
                    show_alert=True
                )
            else:
                await call.answer(text="💸 У вас не хватает денег!", show_alert=True)

        case "friendliness":
            if factory.moneys >= UPGRADE_ENVIRONMENTAL_FRIENDLINESS:
                updated_factory = await update_factory(
                    user_id=user_id,
                    moneys=factory.moneys - UPGRADE_ENVIRONMENTAL_FRIENDLINESS,
                    environmental_friendliness=factory.environmental_friendliness + 1
                )
                await call.answer(
                    text=(
                         "✅ Вы успешно подняли экологичность завода!\n"
                         f"🌱 Экологичность: {updated_factory.environmental_friendliness}/5\n"
                         f"💵 Денег на счете: {updated_factory.moneys}$"
                    ),
                    show_alert=True
                )
            else:
                await call.answer(text="💸 У вас не хватает денег!", show_alert=True)
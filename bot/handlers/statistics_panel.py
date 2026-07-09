from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram import Router, F

from bot.data.database import get_factory_by_owner

statistic_panel_router: Router = Router()

@statistic_panel_router.message(F.text == "📊 Статистика")
async def check_stats(message: Message) -> None:
    user_id = message.from_user.id

    factory = await get_factory_by_owner(user_id)

    if not factory:
        await message.answer("❌ У вас еще нет завода! Используйте /start для регистрации.")
        return

    text: str = (
        f"\t📊 **Статистика** 📈\n\n"
        f"— 🏭 Завод: «{factory.factory_name}»\n"
        f"— 💰 Баланс: {factory.moneys}$\n"
        f"— 👥 Рабочие: {factory.number_of_workers} чел. Счастье: {factory.workers_happiness:.1f}/5\n"
        f"— 🌿 Экологичность: {factory.environmental_friendliness:.1f}/5\n"
        f"— ⚙️ Оборудование: {factory.quality_of_equipment:.1f}/5\n"
        f"— ⚡ Производство: {factory.production_per_hour:.1f} ед./час\n"
        f"— ⭐️ Репутация: {factory.reputation:.1f}\n"
        f"— 🏆 Счет: {factory.score:.1f}"
    )

    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN)
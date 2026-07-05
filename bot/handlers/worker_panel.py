from aiogram import Router, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message, CallbackQuery
from bot.data.database import get_factory_by_owner, update_factory
from bot.keyboards.inline import *

worker_panel_router: Router = Router()

RAISE_WORKER_SALARY: int = 50
PLUS_HAPPINESS_WHEN_SALARY_RAISED: float = 0.3

TEACH_WORKER_PRICE: int = 100
PLUS_QUALITY_OF_PRODUCTS_WHEN_WORKERS_TEACHED: float = 1.0

WORKER_PRICE: int = 500
MINUS_HAPPINESS_WHEN_WORKER_FIRED: float = 0.1

async def show_workers_menu(target: Message, other) -> None:
    factory = await get_factory_by_owner(other.from_user.id)

    if not factory:
        await target.answer("❌ У вас еще нет завода! Используйте /start для регистрации.")
        return
    workers_count = factory.number_of_workers

    await target.answer_photo(
        photo="https://i.pinimg.com/1200x/64/1f/f5/641ff500ca9af0e8d83f5fde557116f2.jpg",
        caption=(
            "👷 **Панель управления рабочими** 🔧\n\n"
            "• Нанять рабочего — `500$` — `+1` рабочий\n"
            "• Уволить рабочего — `0$` — `-0.1` счастья\n"
            f"• Поднять зарплату — `50$/чел` ({workers_count * RAISE_WORKER_SALARY}$) — `+0.3` счастья\n"
            f"• Обучить рабочих — `100$/чел` ({workers_count * TEACH_WORKER_PRICE}) — `+1` качество техники"
        ),
        reply_markup=workers_managing_kb,
        parse_mode=ParseMode.MARKDOWN
    )

@worker_panel_router.message(F.text == "👷 Рабочие")
async def workers_msg_handler(message: Message) -> None:
    await show_workers_menu(message, message)

@worker_panel_router.callback_query(F.data == "to_workers_managing_kb")
async def workers_callback_handler(call: CallbackQuery) -> None:
    await call.answer()
    await show_workers_menu(call.message, call)

@worker_panel_router.callback_query(F.data == "new_worker")
async def new_worker_main(call: CallbackQuery) -> None:
    await call.answer()
    await call.message.edit_caption(
        caption=
            "➕ **Нанять рабочих** 👷\n\n"
            "• Один рабочий — `500$`\n"
            "• Пять рабочих — `2,500$`\n"
            "• Десять рабочих — `5,000$`\n"
            "• Пятьдесят рабочих — `25,000$`"
        ,
        reply_markup=new_worker_kb,
        parse_mode=ParseMode.MARKDOWN
    )

@worker_panel_router.callback_query(F.data == "dismiss_worker")
async def dismiss_worker_main(call: CallbackQuery) -> None:
    await call.answer()
    await call.message.edit_caption(
        caption=
        "➖ **Уволить рабочих** 👷\n\n"
        "• Один рабочий — `0$` — `-0.1` счастья\n"
        "• Пять рабочих — `0$` — `-0.5` счастья\n"
        "• Десять рабочих — `0$` — `-1` счастье"
        ,
        reply_markup=dismiss_worker_kb,
        parse_mode=ParseMode.MARKDOWN
    )

@worker_panel_router.callback_query(F.data == "raise_salary")
async def raise_salary(call: CallbackQuery) -> None:
    factory = await get_factory_by_owner(call.from_user.id)

    if not factory:
        await call.answer(text="❌ У вас еще нет завода! Используйте /start для регистрации.", show_alert=True)
        return
    workers_count = factory.number_of_workers
    moneys = factory.moneys
    price = workers_count * RAISE_WORKER_SALARY

    if moneys < price:
        await call.answer(text="💸У вас нехватает денег!", show_alert=True)
        return

    if factory.workers_happiness <= (5 - PLUS_HAPPINESS_WHEN_SALARY_RAISED) and factory.number_of_workers > 0:
        updated_factory = await update_factory(call.from_user.id, moneys=factory.moneys - price, workers_happiness=factory.workers_happiness + PLUS_HAPPINESS_WHEN_SALARY_RAISED)
        await call.answer(
            text=f"✅ Вы увеличили зарплату рабочих!\n"
                 f"💵 Денег: {updated_factory.moneys}$\n"
                 f"😇 Счастье: {updated_factory.workers_happiness:.1f}/5",
            show_alert=True
        )
    else:
        await call.answer(text="😇У вас максимальный уровень счастья рабочих или нет рабочих!", show_alert=True)

@worker_panel_router.callback_query(F.data == "teach_workers")
async def teach_workers(call: CallbackQuery) -> None:
    factory = await get_factory_by_owner(call.from_user.id)

    if not factory:
        await call.answer(text="❌У вас еще нет завода! Используйте /start для регистрации.", show_alert=True)
        return
    workers_count = factory.number_of_workers
    moneys = factory.moneys
    price = workers_count * TEACH_WORKER_PRICE

    if moneys < price:
        await call.answer(text="💸У вас нехватает денег!", show_alert=True)
        return

    if factory.quality_of_equipment <= (5 - PLUS_QUALITY_OF_PRODUCTS_WHEN_WORKERS_TEACHED) and factory.number_of_workers > 0:
        updated_factory = await update_factory(call.from_user.id, moneys=factory.moneys - price, quality_of_equipments=factory.quality_of_equipment + PLUS_QUALITY_OF_PRODUCTS_WHEN_WORKERS_TEACHED)
        await call.answer(
            text=f"✅ Вы обучили рабочих!\n"
                 f"💵 Денег: {updated_factory.moneys}$\n"
                 f"😇 Качество техники: {updated_factory.workers_happiness}/5",
            show_alert=True
        )
    else:
        await call.answer(text="⚙️У вас максимальный уровень качества техники или нет рабочих!", show_alert=True)

@worker_panel_router.callback_query(F.data.startswith("buy_worker_"))
async def new_worker_count(call: CallbackQuery) -> None:
    count = int(call.data.split("_")[-1])
    factory = await get_factory_by_owner(call.from_user.id)
    if not factory:
        await call.answer(text="❌У вас еще нет завода! Используйте /start для регистрации.", show_alert=True)
        return
    price = count * WORKER_PRICE

    if factory.moneys < price:
        await call.answer(text="💸У вас нехватает денег!", show_alert=True)
        return

    updated_factory = await update_factory(user_id=call.from_user.id, number_of_workers=factory.number_of_workers + count, moneys=factory.moneys - price)
    await call.answer(
        text=f"👷 Вы успешно наняли рабочих (+{count} чел.)!\n"
             f"📊 Всего рабочих: {updated_factory.number_of_workers}\n"
             f"⚡ Производство выросло до: {updated_factory.production_per_hour:.1f}/ч",
        show_alert=True
    )

@worker_panel_router.callback_query(F.data.startswith("delete_worker_"))
async def new_worker_count(call: CallbackQuery) -> None:
    count = int(call.data.split("_")[-1])
    factory = await get_factory_by_owner(call.from_user.id)
    if not factory:
        await call.answer(text="❌У вас еще нет завода! Используйте /start для регистрации.", show_alert=True)
        return
    minus_happiness = count * MINUS_HAPPINESS_WHEN_WORKER_FIRED

    if factory.number_of_workers < count:
        await call.answer(text="❌У вас нет такого кол-ва рабочих!", show_alert=True)

    updated_factory = await update_factory(user_id=call.from_user.id, number_of_workers=factory.number_of_workers - count, workers_happiness=factory.workers_happiness - minus_happiness)
    await call.answer(
        text=f"👷 Вы уволили рабочих (-{count} чел.)!\n"
             f"📊 Всего рабочих: {updated_factory.number_of_workers}\n"
             f"😇 Счастье рабочих упало до: {updated_factory.workers_happiness:.1f}/ч",
        show_alert=True
    )

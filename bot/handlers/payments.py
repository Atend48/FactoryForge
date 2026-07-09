import os
from pathlib import Path

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, LabeledPrice, Message, PreCheckoutQuery
from dotenv import load_dotenv

from bot.data.database import update_factory, get_factory_by_owner
from bot.keyboards.inline import buy_moneys_kb, actions_kb, payments_kb

payment_router: Router = Router()

DIR = Path(__file__).absolute().parent.parent.parent
ENV_PATH = DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")


@payment_router.message(F.text == "⚡ Действие")
async def actions_menu(message: Message) -> None:
    await message.answer(text="Выберите действие:",
                         reply_markup=actions_kb)

@payment_router.callback_query(F.data == "donat")
async def donat(call: CallbackQuery) -> None:
    await call.message.edit_text(text="Выберите донатную услугу:",
                                 reply_markup=payments_kb)

@payment_router.callback_query(F.data == "moneys")
async def main_payment_panel(call: CallbackQuery) -> None:
    await call.message.edit_text(text="Выберите, сколько $ хотите купить",
                                 reply_markup=buy_moneys_kb)
    await call.answer()

@payment_router.callback_query(F.data.startswith("buy_moneys_"))
async def send_eco_invoice(call: CallbackQuery) -> None:
    count = int(call.data.split("_")[-1])

    invoice_price = 100000 if count == 10000 else 500000

    prices = [
        LabeledPrice(label="Покупка денег", amount=invoice_price)
    ]

    dynamic_payload = f"buy_many_moneys:{count}"

    await call.message.answer_invoice(
        title="Покупка денег",
        description=f"Прибавляет {count}$ на счет фабрики",
        payload=dynamic_payload,
        provider_token=PROVIDER_TOKEN,
        currency="KZT",
        prices=prices,
        start_parameter="buy-moneys"
    )
    await call.answer()

@payment_router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@payment_router.message(F.successful_payment)
async def success_payment(message: Message):
    payment_info = message.successful_payment
    payload = payment_info.invoice_payload

    if payload.startswith("buy_many_moneys:"):
        added_moneys = int(payload.split(":")[-1])

        factory = await get_factory_by_owner(message.from_user.id)

        if not factory:
            await message.answer(
                "❌ **Ошибка:** У вас ещё не создана фабрика! "
                "Пожалуйста, введите команду /start, чтобы зарегистрироваться, "
                "после чего администрация начислит вам купленные средства вручную."
            )
            return

        await update_factory(
            user_id=message.from_user.id,
            moneys=factory.moneys + added_moneys
        )

        await message.answer(
            text=(
                "🎉 **Оплата прошла успешно!**\n"
                f"🌿 Вы приобрели {added_moneys}$"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
from pathlib import Path
from aiogram import Router, F
from aiogram.enums import parse_mode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, StateFilter
from bot.data.database import new_user
from bot.keyboards.base_keyboards import NEW_FACTORY

base_commands_router = Router()

start_image_path = Path(__file__).parent.parent / "data" / "start_image.png"
start_image = FSInputFile(str(start_image_path))

@base_commands_router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer_photo(photo=start_image, caption="""
🏭 **Добро пожаловать на Фабрику Техники!**

Вы — молодой предприниматель, который решил построить **империю по производству техники**. 
У вас есть пустой цех, немного денег и огромные амбиции.

🎯 **Ваша цель:** 
Пройти 100 месяцев, развивая фабрику, зарабатывая деньги и завоёвывая репутацию.

📊 **Ваши ресурсы:**
• 💰 Деньги: 10 000 ₽
• 👷 Рабочие: 0
• 🌿 Экология: 0/5
• ⭐ Качество: 0/5
• 😊 Счастье рабочих: 0/5

⚙️ **Что можно делать:**
• Нанять и обучать рабочих
• Улучшать экологию и качество
• Запускать производство
• Продавать технику
• Инвестировать в развитие

📢 **Важно:**
• Каждый месяц (ход) приносит расходы и доходы
• Случайные события могут изменить ход игры
• Балансируйте между прибылью и репутацией

🏆 **Победа:** 
Заработайте максимальный рейтинг за 100 месяцев!

👇 **Начните управление с помощью кнопок ниже:**
    """, parse_mode=parse_mode.ParseMode.MARKDOWN, reply_markup=NEW_FACTORY)

class FactoryReg(StatesGroup):
    name: str = State()

@base_commands_router.message(StateFilter(None), F.text == "🏭 Создать завод")
async def add_factory_fsm(message: Message, state: FSMContext):
    await message.answer(
        text="🏭 Введите название вашего завода"
    )
    await state.set_state(FactoryReg.name)

@base_commands_router.message(FactoryReg.name)
async def add_name(message: Message, state: FSMContext):
    factory_name = message.text  # Берем то, что написал юзер
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"

    try:
        await new_user(
            username=username,
            user_id=user_id,
            factory_name=str(factory_name)
        )

        await message.answer(
            text=f"🏭 Завод «{factory_name}» успешно создан!\nУдачи в управлении!"
        )
        await state.clear()

    except Exception as e:
        await message.answer(text="❌ Произошла ошибка при создании завода. Возможно, вы уже зарегистрированы.")
        print(f"Ошибка БД: {e}")
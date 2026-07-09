from aiogram import Router, F
from aiogram.enums import parse_mode

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter

from bot.data.database import new_user, user_exists, get_user_name, get_factory_name
from bot.keyboards.base_keyboards import NEW_FACTORY, MAIN_KEYBOARD

base_commands_router = Router()

start_image: str = "https://i.pinimg.com/1200x/40/88/9f/40889ffc9788baa9baaa931d00de5b6f.jpg"

@base_commands_router.message(CommandStart())
async def start(message: Message) -> None:
    if await user_exists(message.from_user.id):
        user_id = message.from_user.id
        await message.answer_photo(
            photo=start_image,
            caption=f"👋 С возвращением, {await get_user_name(user_id)}! Ваш завод {await get_factory_name(user_id)} уже вовсю работает.\nИспользуйте меню для управления.",
            reply_markup=MAIN_KEYBOARD
        )
    else:
        await message.answer_photo(photo=start_image, caption="""
🏭 **Добро пожаловать на Фабрику Техники!**
    
Вы — молодой предприниматель, который решил построить **империю по производству техники**. 
У вас есть пустой цех, немного денег и огромные амбиции.
    
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
""", parse_mode=parse_mode.ParseMode.MARKDOWN, reply_markup=NEW_FACTORY)

class FactoryReg(StatesGroup):
    name: str = State()

@base_commands_router.message(StateFilter(None), F.text == "🏭 Создать завод")
async def add_factory_fsm(message: Message, state: FSMContext) -> None:
    await message.answer(
        text="🏭 Введите название вашего завода"
    )
    await state.set_state(FactoryReg.name)

@base_commands_router.message(FactoryReg.name)
async def add_name(message: Message, state: FSMContext) -> None:
    factory_name = message.text
    user_id = message.from_user.id
    username = message.from_user.username or "Unknown"

    try:
        await new_user(
            username=username,
            user_id=user_id,
            factory_name=str(factory_name)
        )

        await message.answer(
            text=f"🏭 Завод «{factory_name}» успешно создан!\nУдачи в управлении!",
            reply_markup=MAIN_KEYBOARD
        )
        await state.clear()

    except Exception as e:
        await message.answer(text="❌ Произошла ошибка при создании завода. Возможно, вы уже зарегистрированы.", reply_markup=MAIN_KEYBOARD)
        print(f"Ошибка БД: {e}")
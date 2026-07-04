from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

START_KEYBOARD = [
        [
            KeyboardButton(text="📊 Статистика"),
            KeyboardButton(text="🏭 Производство")
        ],
        [
            KeyboardButton(text="👷 Рабочие"),
            KeyboardButton(text="🔧 Улучшения")
        ],
        [
            KeyboardButton(text="💰 Продать"),
            KeyboardButton(text="📈 Рынок")
        ],
        [
            KeyboardButton(text="⚡ Действие")
        ]
    ]

MAIN_KEYBOARD: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[*START_KEYBOARD], resize_keyboard=True
)

NEW_FACTORY: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🏭 Создать завод")]],
    resize_keyboard=True
)
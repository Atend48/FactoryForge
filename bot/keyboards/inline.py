from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

workers_managing_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text="💸 Поднять зарплату (50$/чел)", callback_data="raise_salary")
        ],
        [
            InlineKeyboardButton(text="➕ Нанять рабочих (500$)", callback_data="new_worker"),
            InlineKeyboardButton(text="➖ Уволить рабочих (0$)", callback_data="dismiss_worker")
        ],
        [
          InlineKeyboardButton(text="💤 Отправить рабочих отдохнуть (20$/чел)", callback_data="send_the_workers_to_rest")
        ],
        [
            InlineKeyboardButton(text="📕 Обучить рабочих (200$/чел)", callback_data="teach_workers")
        ]
    ]
)

new_worker_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text="1 Рабочий (500$)", callback_data="buy_worker_1"),
            InlineKeyboardButton(text="5 Рабочих (2500$)", callback_data="buy_worker_5")
        ],
        [
            InlineKeyboardButton(text="10 Рабочих (5000$)", callback_data="buy_worker_10"),
            InlineKeyboardButton(text="50 Рабочих (25000$)", callback_data="buy_worker_50")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="to_workers_managing_kb")
        ]
    ]
)

dismiss_worker_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text="1 Рабочий", callback_data="delete_worker_1"),
            InlineKeyboardButton(text="5 Рабочих", callback_data="delete_worker_5")
        ],
        [
            InlineKeyboardButton(text="10 Рабочих", callback_data="delete_worker_10")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="to_workers_managing_kb")
        ]
    ]
)

improvements_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="⚙️ Улучшить качество техники", callback_data="upgrade_quality_of_equipment")
    ],
    [
        InlineKeyboardButton(text="🌿 Поднять экологичность", callback_data="upgrade_environmental_friendliness")
    ]
])

manufacture_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🧑‍🏭 Произвести партию товара", callback_data="make_a_batch")
    ]
])

actions_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="💰 Донат 🤑", callback_data="donat")
    ]
])

sales_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="💵 Продать всю технику", callback_data="sell_all")
    ]
])

payments_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🪙 Купить $$$", callback_data="moneys")
    ]
])

buy_moneys_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="10,000$", callback_data="buy_moneys_10000"),
        InlineKeyboardButton(text="50,000$", callback_data="buy_moneys_50000")
    ]
])
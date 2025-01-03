import asyncio
import os
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, CallbackQuery

# Токен вашего бота
API_TOKEN = '7546669334:AAEGezLeqVQw5mBiYJFeunLo_6Gophpfylc'

# Ссылка на ваш Telegram-контакт
CONTACT_LINK = "https://t.me/Ilya_sidorenk0"
YOUTUBE_LINK = "https://youtube.com/channel/your_channel"
CHANNEL_ID = "@the_top_info_link"  # Ссылка на канал для подписки

# Создаём бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Хранилище языка для пользователей
user_languages = {}

# Функция для получения текущего языка пользователя
def get_user_language(user_id):
    return user_languages.get(user_id, "uk")  # По умолчанию украинский

# Функция для получения перевода текста в зависимости от языка
def get_text(lang, key):
    translations = {
        "uk": {
            "home": "🏠 Домой",
            "partners": "🔗 Партнери",
            "vip": "💎 VIP",
            "news": "📰 Новини",
            "tariffs": "📋 Тарифи",
            "youtube": "▶️ YouTube",
            "change_language": "🌍 Змінити мову",
            "subscribe": "🚀 Підписатися",
            "back": "⬅️ Назад",
            "iban": "💳 Оплата через IBAN",
            "card_number": "💳 Номер картки",
        },
        "ru": {
            "home": "🏠 Домой",
            "partners": "🔗 Партнёры",
            "vip": "💎 VIP",
            "news": "📰 Новости",
            "tariffs": "📋 Тарифы",
            "youtube": "▶️ YouTube",
            "change_language": "🌍 Сменить язык",
            "subscribe": "🚀 Подписаться",
            "back": "⬅️ Назад",
            "iban": "💳 Оплата через IBAN",
            "card_number": "💳 Номер карты",
        },
        "en": {
            "home": "🏠 Home",
            "partners": "🔗 Partners",
            "vip": "💎 VIP",
            "news": "📰 News",
            "tariffs": "📋 Tariffs",
            "youtube": "▶️ YouTube",
            "change_language": "🌍 Change Language",
            "subscribe": "🚀 Subscribe",
            "back": "⬅️ Back",
            "iban": "💳 Payment via IBAN",
            "card_number": "💳 Card Number",
        },
    }
    return translations[lang].get(key, key)

# Главное меню
def get_main_menu(lang="uk"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=get_text(lang, "partners"), callback_data="partners"),
                InlineKeyboardButton(text=get_text(lang, "vip"), callback_data="vip")
            ],
            [
                InlineKeyboardButton(text=get_text(lang, "news"), callback_data="news"),
                InlineKeyboardButton(text=get_text(lang, "tariffs"), callback_data="tariffs")
            ],
            [
                InlineKeyboardButton(text=get_text(lang, "youtube"), url=YOUTUBE_LINK),
                InlineKeyboardButton(text=get_text(lang, "change_language"), callback_data="language")
            ],
            [
                InlineKeyboardButton(text=get_text(lang, "subscribe"), url=CONTACT_LINK),
                InlineKeyboardButton(text=get_text(lang, "home"), callback_data="home")
            ]
        ]
    )

# Подменю тарифов
def get_tariffs_menu(lang="uk"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Тариф 1: 1000 грн", callback_data="tariff_1")],
            [InlineKeyboardButton(text="Тариф 2: 2000 грн", callback_data="tariff_2")],
            [InlineKeyboardButton(text="Тариф 3: 3000 грн", callback_data="tariff_3")],
            [InlineKeyboardButton(text=get_text(lang, "back"), callback_data="home")]
        ]
    )

# Удаление предыдущего меню
async def delete_previous_menu(callback: CallbackQuery):
    try:
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    except:
        pass

# Команда /start
@router.message(F.text == "/start")
async def send_welcome(message: Message):
    user_languages[message.from_user.id] = get_user_language(message.from_user.id)  # Устанавливаем язык по умолчанию
    lang = get_user_language(message.from_user.id)
    
    # Отправляем картинку только один раз
    photo_path = os.path.join(os.getcwd(), "3.png")  # Путь к картинке
    photo = FSInputFile(photo_path)  # Используем FSInputFile для загрузки
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo
    )

    # Главное меню
    main_menu = get_main_menu(lang)
    await message.answer("🔥 Оберіть дію:", reply_markup=main_menu)

# Кнопка "Домой"
@router.callback_query(F.data == "home")
async def home_callback(callback: CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    await delete_previous_menu(callback)

    # Главное меню
    main_menu = get_main_menu(lang)
    await callback.message.answer("🔥 Оберіть дію:", reply_markup=main_menu)
    await callback.answer()

# Кнопка "Сменить язык"
@router.callback_query(F.data == "language")
async def change_language(callback: CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    lang_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Українська", callback_data="set_lang_uk")],
            [InlineKeyboardButton(text="English", callback_data="set_lang_en")],
            [InlineKeyboardButton(text="Русский", callback_data="set_lang_ru")]
        ]
    )
    await callback.message.answer(get_text(lang, "change_language"), reply_markup=lang_menu)
    await callback.answer()

# Установить язык
@router.callback_query(F.data.in_(["set_lang_uk", "set_lang_en", "set_lang_ru"]))
async def set_language(callback: CallbackQuery):
    new_lang = callback.data.split("_")[-1]
    user_languages[callback.from_user.id] = new_lang
    await callback.message.answer(f"🌍 Язык изменён на: {new_lang}.")
    await home_callback(callback)

# Кнопка "VIP"
@router.callback_query(F.data == "vip")
async def show_vip(callback: CallbackQuery):
    # Проверяем подписку
    try:
        user_status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=callback.from_user.id)
        if user_status.status in ("member", "administrator", "creator"):
            # Пользователь подписан, показываем VIP-предложения
            vip_menu = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=get_text(get_user_language(callback.from_user.id), "iban"), callback_data="iban_transfer")],
                    [InlineKeyboardButton(text=get_text(get_user_language(callback.from_user.id), "card_number"), callback_data="card_number_transfer")],
                    [InlineKeyboardButton(text=get_text(get_user_language(callback.from_user.id), "back"), callback_data="home")]
                ]
            )
            await callback.message.answer(
                "💎 VIP-подписка предоставляет доступ к эксклюзивным возможностям:\n"
                "✔️ Доступ к закрытому чату\n"
                "✔️ Еженедельные бонусы\n"
                "✔️ Персональные советы по инвестициям\n\n"
                "Подключитесь и начните зарабатывать с нами!",
                reply_markup=vip_menu
            )
        else:
            # Пользователь не подписан
            vip_promo_menu = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🚀 Подписаться", url=CONTACT_LINK)],
                    [InlineKeyboardButton(text=get_text(get_user_language(callback.from_user.id), "back"), callback_data="home")]
                ]
            )
            await callback.message.answer(
                "💎 Чтобы продолжить, подпишитесь на наш канал! После этого вы получите доступ к VIP-предложениям.",
                reply_markup=vip_promo_menu
            )
    except Exception as e:
        await callback.message.answer("Ошибка при проверке подписки. Попробуйте позже.")
        print(f"Ошибка проверки подписки: {e}")

    await callback.answer()

# Кнопка "Партнёры"
@router.callback_query(F.data == "partners")
async def show_partners(callback: CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    await delete_previous_menu(callback)

    partners_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Партнер {i+1}", url="https://t.me/to_be_on")] for i in range(1, 6)
        ] + [
            [InlineKeyboardButton(text=get_text(lang, "back"), callback_data="home")]
        ]
    )
    await callback.message.answer("🔗 Наші партнери:", reply_markup=partners_menu)
    await callback.answer()

# Кнопка "Новости"
@router.callback_query(F.data == "news")
async def show_news(callback: CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    await delete_previous_menu(callback)

    news_text = (
        "📰 Bitcoin достиг отметки $40,000.\n"
        "📰 Ethereum выпустил обновление Shanghai.\n"
        "📰 Ripple выиграл суд против SEC.\n"
        "📰 Tesla инвестировала $1,5 млрд в криптовалюту.\n"
        "📰 Intel анонсировал чип для майнинга.\n"
        "📰 Binance открывает центр в Абу-Даби.\n"
        "📰 Apple запускает финтех-приложение.\n"
        "📰 Mastercard интегрирует криптовалюты.\n"
        "📰 Fidelity запускает крипто-фонд.\n"
        "📰 Китайский завод увеличил производство блокчейн-чипов."
    )
    news_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(lang, "back"), callback_data="home")]
        ]
    )
    await callback.message.answer(news_text, reply_markup=news_menu)
    await callback.answer()

# Кнопка "Тарифы"
@router.callback_query(F.data == "tariffs")
async def show_tariffs(callback: CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    await delete_previous_menu(callback)

    tariffs_menu = get_tariffs_menu(lang)
    await callback.message.answer("📋 Оберіть тариф:", reply_markup=tariffs_menu)
    await callback.answer()

# Обработка выбора тарифов
@router.callback_query(F.data.in_(["tariff_1", "tariff_2", "tariff_3"]))
async def show_tariff_details(callback: CallbackQuery):
    lang = get_user_language(callback.from_user.id)
    
    tariff_details = {
        "tariff_1": "💰 **Тариф 1**\nЦена: 1000 грн\nОписание: Услуги для малого бизнеса.",
        "tariff_2": "💰 **Тариф 2**\nЦена: 2000 грн\nОписание: Оптимальный выбор для среднего бизнеса.",
        "tariff_3": "💰 **Тариф 3**\nЦена: 3000 грн\nОписание: Премиум услуги для крупных клиентов."
    }
    selected_tariff = tariff_details[callback.data]

    # Кнопка для перехода в VIP
    tariff_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=get_text(lang, "vip"), callback_data="vip")],
            [InlineKeyboardButton(text=get_text(lang, "back"), callback_data="home")]
        ]
    )
    
    await callback.message.answer(selected_tariff, reply_markup=tariff_menu, parse_mode="Markdown")
    await callback.answer()

# Главная функция
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
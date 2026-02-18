import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ================= НАСТРОЙКИ =================

TOKEN = os.getenv("BOT_TOKEN")

STORES = {
    "balaklavskaya": {
        "title": "🍺 ПИНТА — Балаклавская",
        "url": "https://yandex.ru/maps/org/ID/reviews",
        "reviews": [
            "Отличная ПИНТА на Балаклавской, всегда свежее пиво и приятный персонал.",
            "Хороший ассортимент и быстрое обслуживание, рекомендую.",
            "Чисто, уютно, приятно заходить."
        ]
    },
    "kovylnaya": {
        "title": "🍺 ПИНТА — Ковыльная",
        "url": "https://yandex.ru/maps/org/ID/reviews",
        "reviews": [
            "Отличный магазин на Ковыльной, хороший выбор напитков.",
            "Персонал вежливый, пиво всегда свежее.",
            "Приятное место, захожу регулярно."
        ]
    },
    "gagarina": {
        "title": "🍺 ПИНТА — Гагарина",
        "url": "https://yandex.ru/maps/org/ID/reviews",
        "reviews": [
            "Хорошая ПИНТА на Гагарина, удобное расположение.",
            "Большой выбор, всё аккуратно и чисто.",
            "Обслуживание на уровне."
        ]
    },
    "kievskaya": {
        "title": "🍺 ПИНТА — Киевская",
        "url": "https://yandex.ru/maps/org/ID/reviews",
        "reviews": [
            "Отличный магазин на Киевской, приятно заходить.",
            "Всегда свежее пиво и хороший сервис.",
            "Рекомендую эту точку."
        ]
    },
    "leksina": {
        "title": "🍺 ПИНТА — Лексина",
        "url": "https://yandex.ru/maps/org/ID/reviews",
        "reviews": [
            "Удобная ПИНТА рядом с домом, всё нравится.",
            "Хороший выбор и вежливый персонал.",
            "Часто захожу, всегда доволен."
        ]
    },
    "danilova": {
        "title": "🍺 ПИНТА — Данилова",
        "url": "https://yandex.ru/maps/org/ID/reviews",
        "reviews": [
            "Отличный магазин на Данилова, приятная атмосфера.",
            "Всегда свежее пиво и быстрое обслуживание.",
            "Хорошее место."
        ]
    },
    "vorovskogo": {
        "title": "🍺 ПИНТА — Воровского",
        "url": "https://yandex.ru/maps/org/ID/reviews",
        "reviews": [
            "Хорошая ПИНТА на Воровского, всё стабильно.",
            "Ассортимент радует, персонал вежливый.",
            "Захожу регулярно."
        ]
    },
    "polevaya": {
        "title": "🍺 ПИНТА — Полевая",
        "url": "https://yandex.ru/maps/org/ID/reviews",
        "reviews": [
            "Отличная точка на Полевой, чисто и аккуратно.",
            "Приятные продавцы и хороший выбор.",
            "Рекомендую."
        ]
    },
    "molodezhnoe": {
        "title": "🍺 ПИНТА — Молодёжное",
        "url": "https://yandex.ru/maps/org/ID/reviews",
        "reviews": [
            "Хороший магазин в Молодёжном, удобно расположен.",
            "Всегда свежее пиво и нормальные цены.",
            "Приятное обслуживание."
        ]
    },
    "trubochenko": {
        "title": "🍺 ПИНТА — Трубоченко",
        "url": "https://yandex.ru/maps/org/88086573918/reviews",
        "reviews": [
            "Отличный магазин на Трубоченко, всегда свежее пиво и приятное обслуживание.",
            "Хороший выбор напитков, часто захожу именно в эту ПИНТУ.",
            "Уютный магазин, персонал вежливый, ассортимент радует."
        ]
    },
    "konnoi": {
        "title": "🍺 ПИНТА — 1-я Конной армии",
        "url": "https://yandex.ru/maps/org/ID/reviews",
        "reviews": [
            "Отличная ПИНТА на 1-й Конной армии, всегда всё свежее.",
            "Хорошее обслуживание и большой выбор пива.",
            "Приятное место, захожу регулярно."
        ]
    }
}
# ================= КЛАВИАТУРЫ =================

def stores_keyboard():
    buttons = []
    for key, store in STORES.items():
        buttons.append([
            InlineKeyboardButton(
                store["title"],
                callback_data=f"store:{key}"
            )
        ])
    return InlineKeyboardMarkup(buttons)

def review_keyboard(store):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📍 Открыть Яндекс Карты", url=store["url"])],
        [InlineKeyboardButton("🔄 Другой отзыв", callback_data="new_review")],
        [InlineKeyboardButton("🏪 Выбрать другой магазин", callback_data="back_to_stores")]
    ])

# ================= ЛОГИКА =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выбери магазин ПИНТА 👇",
        reply_markup=stores_keyboard()
    )

async def choose_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    store_key = query.data.split(":")[1]
    context.user_data["store"] = store_key

    await send_review(query, context)

async def send_review(update, context):
    store_key = context.user_data["store"]
    store = STORES[store_key]

    review = random.choice(store["reviews"])

    text = (
        f"{store['title']}\n\n"
        "Скопируй отзыв одним нажатием 👇\n\n"
        f"```\n{review}\n```"
    )

    await update.edit_message_text(
        text,
        reply_markup=review_keyboard(store),
        parse_mode="Markdown"
    )

async def new_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await send_review(update.callback_query, context)

async def back_to_stores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Выбери магазин ПИНТА 👇",
        reply_markup=stores_keyboard()
    )

# ================= ЗАПУСК =================

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(choose_store, pattern="^store:"))
    app.add_handler(CallbackQueryHandler(new_review, pattern="new_review"))
    app.add_handler(CallbackQueryHandler(back_to_stores, pattern="back_to_stores"))

    print("✅ Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()

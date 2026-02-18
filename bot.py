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
    "trubochenko": {
        "title": "🍺 ПИНТА — Трубоченко",
        "app_url": "https://yandex.ru/maps/org/88086573918/reviews",
        "web_url": "https://yandex.ru/maps/org/pinta/88086573918/?add-review=true",
        "reviews": [
            "Отличный магазин на Трубоченко, всегда свежее пиво и приятное обслуживание.",
            "Хороший выбор напитков, часто захожу именно в эту ПИНТУ.",
            "Уютный магазин, персонал вежливый, ассортимент радует."
        ]
    },
    "konnoi": {
        "title": "🍺 ПИНТА — 1-я Конной армии",
        "app_url": "https://yandex.ru/maps/org/pinta/22400636893/reviews/?add-review=true&ll=34.074024%2C44.911213&tab=reviews&z=15",
        "web_url": "https://yandex.ru/maps/org/pinta/22400636893/?add-review=true",
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
        [InlineKeyboardButton("📍 Открыть в Яндекс Картах", url=store["app_url"])],
        [InlineKeyboardButton("🌐 Если не открылось — через браузер", url=store["web_url"])],
        [InlineKeyboardButton("🔄 Другой вариант", callback_data="new_review")],
        [InlineKeyboardButton("🏪 Выбрать другой магазин", callback_data="change_store")]
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
    store_key = context.user_data.get("store")
    store = STORES.get(store_key)

    review = random.choice(store["reviews"])

    text = (
        f"{store['title']}\n\n"
        "Скопируй отзыв одним нажатием 👇\n\n"
        f"```\n{review}\n```"
    )

    if hasattr(update, "message"):
        await update.message.reply_text(
            text,
            reply_markup=review_keyboard(store),
            parse_mode="Markdown"
        )
    else:
        await update.edit_message_text(
            text,
            reply_markup=review_keyboard(store),
            parse_mode="Markdown"
        )

async def new_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await send_review(update.callback_query, context)

async def change_store(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "Выбери другой магазин 👇",
        reply_markup=stores_keyboard()
    )

# ================= ЗАПУСК =================

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(choose_store, pattern="^store:"))
    app.add_handler(CallbackQueryHandler(new_review, pattern="new_review"))
    app.add_handler(CallbackQueryHandler(change_store, pattern="change_store"))

    print("✅ Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()

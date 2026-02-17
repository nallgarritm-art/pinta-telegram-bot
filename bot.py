
import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

# ===== НАСТРОЙКИ =====

YANDEX_APP_URL = "yandexmaps://maps.yandex.ru/?oid=88086573918"

REVIEWS = [
    "Отличный пивной магазин! Большой выбор, всё свежее 🍺",
    "Очень приятное место, хороший ассортимент и адекватные цены 👍",
    "Лучший магазин разливного пива в районе, рекомендую 🔥",
    "Всегда свежее пиво и вежливый персонал 🍻",
    "Хожу сюда постоянно, ни разу не разочаровался"
]

# ===== КОМАНДЫ =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    review = random.choice(REVIEWS)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Оставить отзыв", url=YANDEX_REVIEW_URL)],
        [InlineKeyboardButton("🔄 Другой вариант", callback_data="new_review")]
    ])

    await update.message.reply_text(
        f"Вот вариант отзыва:\n\n{review}",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def new_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    review = random.choice(REVIEWS)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Оставить отзыв", url=YANDEX_REVIEW_URL)],
        [InlineKeyboardButton("🔄 Ещё вариант", callback_data="new_review")]
    ])

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        f"Вот другой вариант:\n\n{review}",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# ===== ЗАПУСК =====

def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError("❌ Не задан BOT_TOKEN в Variables Railway")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("review", start))
    app.add_handler(CallbackQueryHandler(new_review, pattern="new_review"))

    print("✅ Bot started")
    app.run_polling()

if __name__ == "__main__":
    main()

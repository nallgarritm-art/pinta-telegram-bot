import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("8579362452:AAGCYcllDu5ULAM6R4-LBZgNRsjGuuyqbBI")

REVIEWS = [
    "Отличный магазин! Всегда свежее пиво и хороший выбор 🍺 Рекомендую!",
    "Очень приятный персонал и большой ассортимент. Захожу постоянно!",
    "Один из лучших пивных магазинов в районе. Качество на уровне!",
    "Хорошие цены, свежее пиво и удобное расположение. 5 звёзд ⭐⭐⭐⭐⭐"
]

YANDEX_REVIEW_URL = "https://yandex.ru/maps/org/pinta/88086573918/reviews/?add-review=true&ll=34.100250%2C44.926224&z=16"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🍻 *Магазин «ПИНТА»*\n\nВыберите любой вариант отзыва и скопируйте его 👇\n\n"
    for i, review in enumerate(REVIEWS, 1):
        text += f"*{i}.* {review}\n\n"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⭐ Оставить отзыв в Яндекс Картах", url=YANDEX_REVIEW_URL)]
    ])

    await update.message.reply_text(
        text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if name == "__main__":
    main()

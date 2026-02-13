from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import random

TOKEN = "8579362452:AAGCYcllDu5ULAM6R4-LBZgNRsjGuuyqbBI"

YANDEX_LINK = "https://yandex.ru/maps/org/pinta/88086573918/reviews/?add-review=true&ll=34.094484%2C44.927617&z=21"

reviews = {
    "short": [
        "Отличный пивной магазин, всегда свежий ассортимент и приятное обслуживание.",
        "Хороший выбор пива, чисто и уютно, персонал вежливый."
    ],
    "medium": [
        "Очень понравился магазин: большой выбор пива, всё свежее, продавцы помогают с выбором.",
        "Хороший магазин с адекватными ценами и приятной атмосферой. Захожу регулярно."
    ],
    "long": [
        "Отличный пивной магазин с большим ассортиментом напитков. Всегда чисто, пиво свежее, персонал вежливый и знающий.",
        "Приятное место для любителей хорошего пива. Ассортимент радует, обслуживание на уровне, хочется возвращаться снова."
    ]
}

async def start(update, context):
    keyboard = [
        [InlineKeyboardButton("✍️ Выбрать текст отзыва", callback_data="choose")]
    ]
    await update.message.reply_text(
        "Спасибо, что выбрали наш магазин 🙌\n"
        "Если не сложно — оставьте отзыв, это очень помогает нам развиваться.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def choose(update, context):
    keyboard = [
        [InlineKeyboardButton("Короткий", callback_data="short")],
        [InlineKeyboardButton("Средний", callback_data="medium")],
        [InlineKeyboardButton("Развёрнутый", callback_data="long")]
    ]
    await update.callback_query.message.reply_text(
        "Выберите формат отзыва:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def send_review(update, context):
    key = update.callback_query.data
    text = random.choice(reviews[key])

    await update.callback_query.message.reply_text(
        f"Вот вариант отзыва:\n\n{text}"
    )

    await update.callback_query.message.reply_text(
        "Нажмите кнопку ниже, чтобы оставить отзыв:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Оставить отзыв ⭐⭐⭐⭐⭐", url=YANDEX_LINK)]
        ])
    )

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(choose, pattern="choose"))
app.add_handler(CallbackQueryHandler(send_review, pattern="short|medium|long"))

app.run_polling()
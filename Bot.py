from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
)
import logging

# 🔒 Укажи свой Telegram ID (узнай через @userinfobot)
ADMIN_CHAT_ID = 6992324436  # ← ЗАМЕНИ на свой ID

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния диалога
WAITING_FOR_QUESTION = 1
user_joined = False  # Флаг, что ты подключился к чату

# Ответы на вопросы
RESPONSES = {
    "1": "В объявлении указана максимально возможная скидка на данный товар, цены в магазине выставляются следующим образом: оцениваются внешний вид устройства, длительность его эксплуатации и техническая составляющая, после всех проверок выставляется цена и сумма скидки!",
    "2": "Мы работаем с 10:00 до 21:00 без выходных!",
    "3": "Доставка возможна по всей России, в зависимости от габаритов товара может доставить через личную службу логистики, или отправить через СДЭК за наш счёт!",
    "4": "Оплатить можно наличными или картой при получении, но при оплате наличными, скидка максимальна!",
    "5": "Свяжемся с вами в течение 15 минут!",
}

# Текст меню с вопросами
MENU_TEXT = (
    "Привет! Это бот автоответчик. Я скоро подключусь к разговору.\n\n"
    "Выберите цифру вопроса, который вас интересует:\n"
    "1. Какие есть скидки?\n"
    "2. Режим работы?\n"
    "3. Есть ли доставка?\n"
    "4. Как оплатить?\n"
    "5. Когда свяжетесь?"
)

# Клавиатура с кнопками
keyboard = [
    [InlineKeyboardButton("1", callback_data="1"),
     InlineKeyboardButton("2", callback_data="2"),
     InlineKeyboardButton("3", callback_data="3")],
    [InlineKeyboardButton("4", callback_data="4"),
     InlineKeyboardButton("5", callback_data="5")]
]
reply_markup = InlineKeyboardMarkup(keyboard)


# Старт — отправляем меню с текстом вопросов и кнопками
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global user_joined
    user_joined = False
    await update.message.reply_text(MENU_TEXT, reply_markup=reply_markup)
    return WAITING_FOR_QUESTION


# Обработка нажатия кнопки — показываем ответ и пересылаем владельцу
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global user_joined
    query = update.callback_query
    await query.answer()  # чтобы убрать "часики" в Telegram

    user_name = query.from_user.full_name
    user_id = query.from_user.id
    user_link = f"[{user_name}](tg://user?id={user_id})"

    question_key = query.data
    response = RESPONSES.get(question_key, "Пожалуйста, выбери цифру от 1 до 5.")
    question_text = {
        "1": "Какие есть скидки?",
        "2": "Режим работы?",
        "3": "Есть ли доставка?",
        "4": "Как оплатить?",
        "5": "Когда свяжетесь?"
    }.get(question_key, "Неизвестный вопрос")

    # Отправляем владельцу сообщение с кликабельной ссылкой и текстом вопроса
    await context.bot.send_message(
        chat_id=6992324436,
        text=f"📩 Сообщение от {user_link}:\nВопрос: {question_text}",
        parse_mode="Markdown"
    )

    # Ответ пользователю (отправляем только ответ, но кнопки оставляем!)
    await query.edit_message_text(text=f"{MENU_TEXT}\n\nВаш выбор: {question_key}\n\n{response}",
                                  reply_markup=reply_markup)
    return WAITING_FOR_QUESTION


# Команда /join — ты подключаешься, отключая автоответчик
async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global user_joined
    user_joined = True
    await update.message.reply_text("Вы подключились. Автоответчик выключен.")
    return ConversationHandler.END


def main():
    TOKEN = "7727193865:AAHpMSfqimZ7UJqgH8SYzPHHEzFzWJz3Iw0"  # Заменить на свой токен

    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_FOR_QUESTION: [CallbackQueryHandler(button_handler)]
        },
        fallbacks=[CommandHandler("join", stop_bot)],
    )

    app.add_handler(conv_handler)
    print("🤖 Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
import sys
import os
import django
from dotenv import load_dotenv
import telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from django.conf import settings
from asgiref.sync import sync_to_async

# Загрузка переменных из .env файла
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(project_path, '.env'))

# Установка пути к проекту и инициализация Django
if project_path not in sys.path:
    sys.path.append(project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')
django.setup()

# Создаем экземпляр бота
bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

# Роли пользователей
USER_ROLE = "user"
MANAGER_ROLE = "manager"


# Функция для привязки пользователя по номеру телефона
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    chat_id = update.message.chat.id
    if contact:
        phone_number = contact.phone_number
        user_role = MANAGER_ROLE if phone_number.endswith("00") else USER_ROLE  # Пример условия для менеджера
        context.user_data["role"] = user_role
        await bot.send_message(chat_id=chat_id, text=f"Ваш номер {phone_number} подтвержден.\nРоль: {user_role}.")
        await show_menu(update, context)


# Отображение меню для пользователей и менеджеров
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_role = context.user_data.get("role", USER_ROLE)
    if user_role == MANAGER_ROLE:
        # Меню для менеджера
        keyboard = [
            [KeyboardButton("📈 Отчет по заказам")],
            [KeyboardButton("📋 Проверить все заказы")],
            [KeyboardButton("🔄 Главное меню")]
        ]
        welcome_text = "Добро пожаловать, менеджер! 👩‍💼"
    else:
        # Меню для пользователя
        keyboard = [
            [KeyboardButton("🛍️ Создать заказ")],
            [KeyboardButton("📦 Мои заказы")],
            [KeyboardButton("🔄 Главное меню")]
        ]
        welcome_text = "Добро пожаловать! 👋 Выберите действие:"

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await bot.send_message(chat_id=chat_id, text=welcome_text, reply_markup=reply_markup)


# Функция обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    keyboard = [
        [KeyboardButton("📞 Подтвердить номер телефона", request_contact=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await bot.send_message(chat_id=chat_id, text="Пожалуйста, подтвердите ваш номер телефона:",
                           reply_markup=reply_markup)


# Функция создания заказа
async def create_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await bot.send_message(chat_id=chat_id, text="🛒 Создание заказа...")

    # Пример каталога
    catalog = "1️⃣ Букет Роз - 1500 руб.\n2️⃣ Орхидеи - 2500 руб.\n3️⃣ Лилии - 2000 руб."
    await bot.send_message(chat_id=chat_id, text=f"Каталог товаров:\n\n{catalog}\n\nНапишите ID цветка и количество.")


# Функция для проверки заказов
async def check_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_role = context.user_data.get("role", USER_ROLE)
    chat_id = update.effective_chat.id

    if user_role == MANAGER_ROLE:
        await bot.send_message(chat_id=chat_id, text="📋 Все заказы:\n1. Букет Роз (Ожидает)\n2. Лилии (Доставлен)")
    else:
        await bot.send_message(chat_id=chat_id, text="📦 Ваши заказы:\n1. Букет Роз (В пути)\n2. Орхидеи (Ожидает)")


# Функция для отправки отчета по заказам
async def send_order_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await bot.send_message(chat_id=chat_id, text="📊 Минуточку, готовлю отчет...")
    report_message = "🧾 Отчет по заказам:\n\nОбщий доход: 10000 руб.\nЗаказов выполнено: 5\nВ процессе: 3"
    await bot.send_message(chat_id=chat_id, text=report_message)


# Основная функция запуска бота
def main():
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        print("Ошибка: Необходимо установить переменную окружения TELEGRAM_BOT_TOKEN с токеном бота")
        return

    application = ApplicationBuilder().token(bot_token).build()

    # Добавляем обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    application.add_handler(MessageHandler(filters.Regex("^(🛍️ Создать заказ)$"), create_order))
    application.add_handler(MessageHandler(filters.Regex("^(📦 Мои заказы|📋 Проверить все заказы)$"), check_orders))
    application.add_handler(MessageHandler(filters.Regex("^(📈 Отчет по заказам)$"), send_order_report))
    application.add_handler(MessageHandler(filters.Regex("^(🔄 Главное меню)$"), show_menu))

    application.run_polling()


if __name__ == '__main__':
    main()

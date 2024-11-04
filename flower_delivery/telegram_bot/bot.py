import sys
import os
import django
from dotenv import load_dotenv
import telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
from django.conf import settings

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


# Функция для привязки пользователя по номеру телефона
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    chat_id = update.message.chat.id
    if contact:
        phone_number = contact.phone_number
        user_role = "manager" if phone_number.endswith("00") else "user"
        context.user_data["role"] = user_role
        await bot.send_message(chat_id=chat_id, text=f"Ваш номер {phone_number} подтвержден.\nРоль: {user_role}.")
        await show_menu(update, context)


# Отображение меню для пользователей и менеджеров
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_role = context.user_data.get("role", "user")
    if user_role == "manager":
        keyboard = [
            [KeyboardButton("📈 Отчет по заказам")],
            [KeyboardButton("📋 Проверить все заказы")],
            [KeyboardButton("🔄 Главное меню")]
        ]
        welcome_text = "Добро пожаловать, менеджер! 👩‍💼"
    else:
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


# Функция создания заказа с заглушкой каталога
async def create_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await bot.send_message(chat_id=chat_id, text="🛒 Выберите цветок для заказа:")

    # Статичный каталог для примера
    catalog_items = [
        {"id": 1, "name": "Букет Роз", "price": "1500 руб.", "photo_url": "https://example.com/rose.jpg"},
        {"id": 2, "name": "Орхидеи", "price": "2500 руб.", "photo_url": "https://example.com/orchid.jpg"},
        {"id": 3, "name": "Лилии", "price": "2000 руб.", "photo_url": "https://example.com/lily.jpg"}
    ]
    keyboard = [
        [InlineKeyboardButton(f"{item['name']} - {item['price']}", callback_data=f"select_{item['id']}")]
        for item in catalog_items
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await bot.send_message(chat_id=chat_id, text="Каталог:", reply_markup=reply_markup)


# Обработчик выбора цветка из каталога с заглушкой фото
async def flower_selection_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    flower_id = int(query.data.split('_')[1])

    # Находим цветок из статичного каталога
    catalog_items = {
        1: {"name": "Букет Роз", "price": "1500 руб.", "photo_url": "https://example.com/rose.jpg"},
        2: {"name": "Орхидеи", "price": "2500 руб.", "photo_url": "https://example.com/orchid.jpg"},
        3: {"name": "Лилии", "price": "2000 руб.", "photo_url": "https://example.com/lily.jpg"}
    }
    flower = catalog_items.get(flower_id)
    if flower:
        await bot.send_photo(
            chat_id=query.message.chat.id,
            photo=flower["photo_url"],
            caption=f"Вы выбрали {flower['name']}.\nЦена: {flower['price']}\nДля подтверждения заказа отправьте 'подтвердить'."
        )
        context.user_data["selected_flower"] = flower


# Функция подтверждения заказа
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    flower = context.user_data.get("selected_flower")
    if flower:
        await bot.send_message(chat_id=chat_id, text=f"Ваш заказ на {flower['name']} оформлен! 🎉")
        context.user_data.pop("selected_flower", None)
    else:
        await bot.send_message(chat_id=chat_id, text="Сначала выберите цветок для заказа.")


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
    application.add_handler(CallbackQueryHandler(flower_selection_handler, pattern="^select_\\d+$"))
    application.add_handler(MessageHandler(filters.Regex("^(подтвердить)$"), confirm_order))
    application.add_handler(MessageHandler(filters.Regex("^(📈 Отчет по заказам)$"), send_order_report))
    application.add_handler(MessageHandler(filters.Regex("^(🔄 Главное меню)$"), show_menu))

    application.run_polling()


if __name__ == '__main__':
    main()

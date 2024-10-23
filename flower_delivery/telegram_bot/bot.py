import sys
import os
import django

# Добавляем путь к корневой директории проекта и приложениям
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))  # Корневая директория
sys.path.append(os.path.join(os.path.dirname(__file__), '../orders'))  # Приложение orders
sys.path.append(os.path.join(os.path.dirname(__file__), '../catalog'))  # Приложение catalog

# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')

# Инициализируем Django
django.setup()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from telegram import InputMediaPhoto
from django.conf import settings
from asgiref.sync import sync_to_async
from orders.models import Order
from catalog.models import Flower

# Переменные для хранения временных данных о заказе
user_data = {}

# Начало работы
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Создаем инлайн-кнопки
    keyboard = [
        [InlineKeyboardButton("Создать заказ", callback_data='new_order')],
        [InlineKeyboardButton("Проверить заказы", callback_data='get_orders')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Добро пожаловать! Выберите действие:", reply_markup=reply_markup)

# Обработка кнопок
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'new_order':
        await show_catalog(update, context)
    elif query.data == 'get_orders':
        await get_orders(update, context)

# Показ каталога с цветами
async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    flowers = await sync_to_async(list)(Flower.objects.all())
    if flowers:
        keyboard = []
        for flower in flowers:
            keyboard.append([InlineKeyboardButton(f"{flower.name} - {flower.price} руб.",
                                                  callback_data=f"select_flower_{flower.id}")])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text("Выберите цветок из каталога:", reply_markup=reply_markup)
    else:
        await update.callback_query.message.reply_text("Каталог пуст.")

# Обработка выбора цветка
async def handle_flower_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    flower_id = int(query.data.split("_")[2])
    flower = await sync_to_async(Flower.objects.get)(id=flower_id)

    if flower:
        # Путь к изображению
        image_path = os.path.join(settings.MEDIA_ROOT, flower.image.name)

        # Проверяем, существует ли изображение
        if os.path.exists(image_path):
            with open(image_path, 'rb') as image_file:
                await query.message.reply_photo(photo=image_file, caption=f"{flower.name}\nЦена: {flower.price} руб.")
        else:
            await query.message.reply_text("Изображение недоступно.")

        # Сохраняем информацию о выбранном цветке
        user_id = query.from_user.id
        user_data[user_id] = {"flower": flower}
        await query.message.reply_text("Введите количество:")
    else:
        await query.message.reply_text("Цветок не найден.")

# Получаем количество от пользователя
async def get_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_data and "flower" in user_data[user_id]:
        try:
            quantity = int(update.message.text)
            user_data[user_id]["quantity"] = quantity
            await update.message.reply_text(f"Вы выбрали {quantity} шт.\nВведите адрес доставки:")
        except ValueError:
            await update.message.reply_text("Пожалуйста, введите корректное количество.")

# Получаем адрес от пользователя
async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_data and "quantity" in user_data[user_id]:
        user_data[user_id]["address"] = update.message.text
        await update.message.reply_text("Введите дату доставки (в формате ГГГГ-ММ-ДД):")

# Получаем дату доставки
async def get_delivery_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_data and "address" in user_data[user_id]:
        user_data[user_id]["delivery_date"] = update.message.text

        flower = user_data[user_id]["flower"]
        quantity = user_data[user_id]["quantity"]
        total_price = flower.price * quantity
        address = user_data[user_id]["address"]
        delivery_date = user_data[user_id]["delivery_date"]

        # Создаем заказ
        order = await sync_to_async(Order.objects.create)(
            user_id=user_id, delivery_address=address, delivery_date=delivery_date, status='new',
            total_price=total_price
        )

        # Добавляем цветок в заказ
        await sync_to_async(order.items.create)(flower=flower, quantity=quantity)

        await update.message.reply_text(
            f"Ваш заказ создан!\nЗаказ #{order.id}\nАдрес: {address}\nДата доставки: {delivery_date}\nСумма: {total_price} руб.")

        # Очищаем временные данные
        user_data.pop(user_id)

# Функция для получения заказов пользователя
async def get_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    orders = await sync_to_async(list)(Order.objects.filter(user_id=user_id))

    if orders:
        response_message = "Ваши заказы:\n"
        for order in orders:
            response_message += (f"Заказ #{order.id}:\n"
                                 f"Адрес доставки: {order.delivery_address}\n"
                                 f"Дата доставки: {order.delivery_date}\n"
                                 f"Статус: {order.status}\n\n")
        await update.callback_query.message.reply_text(response_message)
    else:
        await update.callback_query.message.reply_text("У вас нет активных заказов.")

def main():
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("Ошибка: Необходимо установить переменную окружения TELEGRAM_BOT_TOKEN с токеном бота")
        return

    application = ApplicationBuilder().token(bot_token).build()

    # Добавляем обработчики команд и инлайн-кнопок
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(CallbackQueryHandler(handle_flower_selection, pattern="select_flower_"))
    application.add_handler(MessageHandler(filters.Regex(r"^\d+$"), get_quantity))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_address))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_delivery_date))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()

import os
import sys
import django
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Устанавливаем путь к настройкам Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')
# Инициализируем Django
django.setup()


from orders.models import Order
from catalog.models import Flower
from asgiref.sync import sync_to_async


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для обработки заказов. Доступные команды:\n"
                                    "/new_order - создать новый заказ\n"
                                    "/order_status - проверить статус заказа")


async def get_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    orders = Order.objects.all()
    if orders:
        message = "\n".join(
            [f"Заказ #{order.id}, адрес: {order.delivery_address}, статус: {order.status}" for order in orders])
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Нет доступных заказов.")


async def new_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    # Используем sync_to_async для вызова синхронных методов Django
    flower = await sync_to_async(Flower.objects.first)()  # Для упрощения возьмем первый цветок из каталога
    if flower:
        order = await sync_to_async(Order.objects.create)(
            user_id=1, delivery_address="Улица Пушкина, дом Колотушкина", status='new'
        )  # Примерный адрес
        await sync_to_async(order.flowers.add)(flower)

        await update.message.reply_text(f"Новый заказ создан: Заказ #{order.id}, статус: {order.status}")
    else:
        await update.message.reply_text("Нет доступных цветов для заказа.")


from asgiref.sync import sync_to_async

async def order_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:  # Проверяем, переданы ли аргументы
        order_id = context.args[0]
        try:
            # Используем sync_to_async для работы с синхронными методами
            order = await sync_to_async(Order.objects.get)(id=order_id)
            await update.message.reply_text(f"Заказ #{order.id}, статус: {order.status}")
        except Order.DoesNotExist:
            await update.message.reply_text(f"Заказ с ID {order_id} не найден.")
    else:
        await update.message.reply_text("Пожалуйста, укажите ID заказа. Пример: /order_status 1")

def main():
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("Ошибка: Необходимо установить переменную окружения TELEGRAM_BOT_TOKEN с токеном бота")
        return
        # Создаем приложение бота с указанным токеном
    application = ApplicationBuilder().token(bot_token).build()

        # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_orders", get_orders))
    application.add_handler(CommandHandler("new_order", new_order))
    application.add_handler(CommandHandler("order_status", order_status))

        # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
        main()
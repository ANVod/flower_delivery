import sys
import os
import django
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from django.conf import settings
from asgiref.sync import sync_to_async
from orders.models import Order
from django.db.models import Sum, Count

# Установка пути к проекту и инициализация Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_delivery.settings')
django.setup()

# Функция для отправки отчета по заказам в Telegram
async def send_order_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = update.effective_chat.id
    bot = telegram.Bot(token=bot_token)

    # Собираем данные для отчета
    total_revenue = await sync_to_async(Order.objects.aggregate)(Sum('total_price'))['total_price__sum'] or 0
    order_status = await sync_to_async(Order.objects.values)('status').annotate(count=Count('id'))

    # Формируем сообщение с отчетом
    report_message = f"Отчет по заказам:\n\nОбщий доход: {total_revenue} руб.\n\nСтатусы заказов:\n"
    for status in order_status:
        report_message += f"{status['status']}: {status['count']} заказов\n"

    await bot.send_message(chat_id=chat_id, text=report_message)

# Основная функция запуска бота
def main():
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("Ошибка: Необходимо установить переменную окружения TELEGRAM_BOT_TOKEN с токеном бота")
        return

    application = ApplicationBuilder().token(bot_token).build()

    # Добавляем обработчик команды для получения отчета
    application.add_handler(CommandHandler("report", send_order_report))
    application.run_polling()

if __name__ == '__main__':
    main()

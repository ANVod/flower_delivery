from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import telegram
from orders.models import Order, OrderItem
from django.conf import settings

# Создаем экземпляр бота
bot = telegram.Bot(token='YOUR_BOT_TOKEN')

# Обработка запросов от Telegram
@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        update = telegram.Update.de_json(request.body.decode('utf-8'), bot)
        chat_id = update.message.chat.id
        text = update.message.text

        # Обработка команд
        if text == '/start':
            bot.send_message(chat_id=chat_id, text="Добро пожаловать! Я помогу вам управлять вашими заказами.")
        elif text == '/status':
            orders = Order.objects.filter(user__telegram_chat_id=chat_id)
            if orders.exists():
                status_list = "\n".join([f"Заказ #{order.id}: {order.status}" for order in orders])
                bot.send_message(chat_id=chat_id, text=f"Ваши заказы:\n{status_list}")
            else:
                bot.send_message(chat_id=chat_id, text="У вас пока нет заказов.")
        elif text.startswith('/order'):
            # Обработка создания заказа
            order_data = text.split()
            if len(order_data) == 3:
                flower_id = order_data[1]
                quantity = order_data[2]
                try:
                    flower = Flower.objects.get(id=flower_id)
                    OrderItem.objects.create(
                        flower=flower,
                        quantity=quantity,
                        order=Order.objects.create(user=update.message.from_user)
                    )
                    bot.send_message(chat_id=chat_id, text="Ваш заказ успешно создан.")
                except Flower.DoesNotExist:
                    bot.send_message(chat_id=chat_id, text="Цветок не найден.")
            else:
                bot.send_message(chat_id=chat_id, text="Используйте команду в формате: /order <ID цветка> <количество>")

    return JsonResponse({'status': 'ok'})


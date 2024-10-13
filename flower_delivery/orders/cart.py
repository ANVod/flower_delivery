from decimal import Decimal
from django.conf import settings
from catalog.models import Flower

class Cart:
    def __init__(self, request):
        """
        Инициализируем корзину пользователя.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, flower, quantity=1, override_quantity=False):
        """
        Добавление товара в корзину или обновление количества товара.
        """
        flower_id = str(flower.id)
        if flower_id not in self.cart:
            self.cart[flower_id] = {'quantity': 0, 'price': str(flower.price)}
        if override_quantity:
            self.cart[flower_id]['quantity'] = quantity
        else:
            self.cart[flower_id]['quantity'] += quantity
        self.save()

    def save(self):
        # помечаем сессию как "измененную"
        self.session.modified = True

    def remove(self, flower):
        """
        Удаление товара из корзины.
        """
        flower_id = str(flower.id)
        if flower_id in self.cart:
            del self.cart[flower_id]
            self.save()

    def __iter__(self):
        flower_ids = self.cart.keys()
        flowers = Flower.objects.filter(id__in=flower_ids)
        cart = self.cart.copy()
        for flower in flowers:
            cart[str(flower.id)]['flower'] = flower
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

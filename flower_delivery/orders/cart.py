from django.conf import settings
from catalog.models import Flower

class Cart:
    def __init__(self, request):
        """ Инициализация корзины. """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, flower, quantity=1, override_quantity=False):
        """ Добавление товара в корзину или изменение его количества. """
        flower_id = str(flower.id)
        if flower_id not in self.cart:
            self.cart[flower_id] = {'quantity': 0, 'price': str(flower.price)}
        if override_quantity:
            self.cart[flower_id]['quantity'] = quantity
        else:
            self.cart[flower_id]['quantity'] += quantity
        self.save()

    def save(self):
        """ Помечает сессию как изменённую для сохранения изменений. """
        self.session.modified = True

    def remove(self, flower):
        """ Удаление товара из корзины. """
        flower_id = str(flower.id)
        if flower_id in self.cart:
            del self.cart[flower_id]
            self.save()

    def __iter__(self):
        """ Перебор элементов корзины и получение связанных объектов товаров. """
        flower_ids = self.cart.keys()
        flowers = Flower.objects.filter(id__in=flower_ids)
        for flower in flowers:
            self.cart[str(flower.id)]['flower'] = flower
            self.cart[str(flower.id)]['total_price'] = float(self.cart[str(flower.id)]['price']) * self.cart[str(flower.id)]['quantity']
            yield self.cart[str(flower.id)]

    def __len__(self):
        """ Возвращает общее количество товаров в корзине. """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """ Возвращает общую стоимость товаров в корзине. """
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """ Полностью очищает корзину. """
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()

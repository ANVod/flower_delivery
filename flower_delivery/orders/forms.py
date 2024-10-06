from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['flowers', 'total_price']


class ModelForm:
    pass
from django import forms
from webapp.models import Product, Order


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Найти')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "phone", "address"]

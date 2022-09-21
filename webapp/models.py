from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, F

DEFAULT_CATEGORY = 'other'
CATEGORY_CHOICES = (
    (DEFAULT_CATEGORY, 'Разное'),
    ('food', 'Еда'),
    ('tech', 'Бытовая техника'),
    ('tools', 'Инструменты'),
    ('toys', 'Игрушки'),
)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Описание')
    category = models.CharField(max_length=20, default=DEFAULT_CATEGORY, choices=CATEGORY_CHOICES,
                                verbose_name='Категория')
    amount = models.PositiveIntegerField(verbose_name='Остаток')
    price = models.DecimalField(verbose_name='Цена', max_digits=7, decimal_places=2,
                                validators=(MinValueValidator(0),))

    def __str__(self):
        return f'{self.name} - {self.amount}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    phone = models.CharField(max_length=30, verbose_name='Телефон')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    products = models.ManyToManyField('webapp.Product', related_name='orders', verbose_name='Товары',
                                      through='webapp.OrderProduct', through_fields=['order', 'product'])
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="orders",
                             verbose_name='Пользователь', null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.phone}'

    def get_total(self):
        total = self.order_products.aggregate(total=Sum(F("qty") * F("product__price")))
        print(total)
        return total["total"]

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProduct(models.Model):
    product = models.ForeignKey('webapp.Product', on_delete=models.CASCADE,
                                verbose_name='Товар', related_name='order_products')
    order = models.ForeignKey('webapp.Order', on_delete=models.CASCADE,
                              verbose_name='Заказ', related_name='order_products')
    qty = models.PositiveIntegerField(verbose_name='Количество')

    def __str__(self):
        return f'{self.product.name} - {self.order.name}'

    def get_sum(self):
        return self.qty * self.product.price

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

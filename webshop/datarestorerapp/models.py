from django.db import models


class ShopUser(models.Model):
    ip = models.CharField(
        verbose_name='ip адрес',
        max_length=15,
        unique=True,
        db_index=True,
    )
    country = models.CharField(
        verbose_name='страна',
        max_length=128,
    )

    def __str__(self):
        return f'{self.ip} - {self.country}'

    class Meta:
        verbose_name = 'shop user'
        verbose_name_plural = 'shop users'


class ProductCategory(models.Model):
    name = models.CharField(
        verbose_name='название категории',
        max_length=64,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='название продукта',
        max_length=128,
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True,
    )
    price = models.DecimalField(
        verbose_name='стоимость',
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'


class Order(models.Model):
    id = models.PositiveBigIntegerField(
        verbose_name='id',
        primary_key=True,
        unique=True,
    )
    user = models.ForeignKey(
        ShopUser,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
    )
    is_paid = models.BooleanField(
        verbose_name='статус оплаты',
        default=0,
    )
    created_at = models.DateTimeField(
        verbose_name='создан',
    )
    updated_at = models.DateTimeField(
        verbose_name='обновлен',
    )

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'


class OrderItem(models.Model):
    order_id = models.ForeignKey(
        Order,
        verbose_name='заказ',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='название продукта',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name='количество',
        default=0,
    )
    created_at = models.DateTimeField(
        verbose_name='создан',
    )

    def __str__(self):
        return f'{self.order_id} - product: {self.product}, quantity: {self.amount}'

    class Meta:
        verbose_name = 'order item'
        verbose_name_plural = 'order items'


class ShopUserAction(models.Model):
    user = models.ForeignKey(
        ShopUser,
        verbose_name='ip адрес',
        on_delete=models.CASCADE,
    )
    action = models.CharField(
        verbose_name='действие пользователя',
        max_length=32,
    )
    created_at = models.DateTimeField(
        verbose_name='создан',
    )

    class Meta:
        verbose_name = 'user action'
        verbose_name_plural = 'user actions'

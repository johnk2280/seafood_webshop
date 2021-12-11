from django.contrib import admin

from .models import (
    ShopUser,
    Product,
    ProductCategory,
    Order,
    OrderItem,
    ShopUserAction,
)

admin.site.register(ShopUser)
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShopUserAction)

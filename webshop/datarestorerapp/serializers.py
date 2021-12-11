from rest_framework import serializers

from datarestorerapp.models import (
    ShopUser,
    Product,
    ProductCategory,
    Order,
    OrderItem,
    ShopUserAction,
)


class ShopUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        fields = (
            'ip',
            'country'
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class ShopUserActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUserAction
        fields = '__all__'

# Generated by Django 3.2.9 on 2021-12-11 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.PositiveBigIntegerField(primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('is_paid', models.BooleanField(default=0, verbose_name='статус оплаты')),
                ('created_at', models.DateTimeField(verbose_name='создан')),
                ('updated_at', models.DateTimeField(verbose_name='обновлен')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='название категории')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='ShopUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(db_index=True, max_length=15, unique=True, verbose_name='ip адрес')),
                ('country', models.CharField(max_length=128, verbose_name='страна')),
            ],
            options={
                'verbose_name': 'shop user',
                'verbose_name_plural': 'shop users',
            },
        ),
        migrations.CreateModel(
            name='ShopUserAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=32, verbose_name='действие пользователя')),
                ('created_at', models.DateTimeField(verbose_name='создан')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datarestorerapp.shopuser', verbose_name='ip адрес')),
            ],
            options={
                'verbose_name': 'user action',
                'verbose_name_plural': 'user actions',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='название продукта')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='стоимость')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datarestorerapp.productcategory', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='количество')),
                ('created_at', models.DateTimeField(verbose_name='создан')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datarestorerapp.order', verbose_name='заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datarestorerapp.product', verbose_name='название продукта')),
            ],
            options={
                'verbose_name': 'order item',
                'verbose_name_plural': 'order items',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datarestorerapp.shopuser', verbose_name='пользователь'),
        ),
    ]

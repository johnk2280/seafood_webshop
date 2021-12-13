import sqlite3
from webshop.settings import BASE_DIR

PATH_TO_DB = BASE_DIR.joinpath('db.sqlite3')


def get_country_by_users() -> list:
    """
    1. Посетители из какой страны чаще всего посещают сайт?

    :return:
    """
    with sqlite3.connect(PATH_TO_DB) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT country, count() as cnt
            FROM datarestorerapp_shopuseraction ds
            JOIN datarestorerapp_shopuser ds2
            ON ds.user_id = ds2.id
            GROUP BY ds2.country
            ORDER BY COUNT(ds2.country) DESC
            """
        )

        return cursor.fetchall()


def get_country_by_category(category='fresh_fish') -> list:
    """
    2. Посетители из какой страны чаще всего интересуются товарами из
    определенной категории “fresh_fish”?

    :param category:
    :return:
    """
    with sqlite3.connect(PATH_TO_DB) as connection:
        cursor = connection.cursor()

        cursor.execute(
            f"""
            SELECT country, COUNT() as cnt
            FROM datarestorerapp_shopuser ds2
            JOIN (
                SELECT user_id
                FROM datarestorerapp_shopuseraction ds
                WHERE category_id = (
                    SELECT id 
                    FROM datarestorerapp_productcategory dp
                    WHERE name = '{category}'
                    )
            ) as tab1
            ON ds2.id = tab1.user_id
            GROUP BY country
            ORDER BY COUNT(country) DESC
            """
        )

        return cursor.fetchall()


def get_time_of_day_by_category(category='frozen_fish'):
    """
    3. В какое время суток чаще всего просматривают категорию “frozen_fish”?

    0 - ночь 00.00 - 05.59
    1 - утро 06.00 - 11.59
    2 - день 12.00 - 17.59
    3 - вечер 18.00 - 23.59

    :param category:
    :return:
    """
    with sqlite3.connect(PATH_TO_DB) as connection:
        cursor = connection.cursor()

        cursor.execute(
            f"""
            SELECT
                (TIME(created_at) / 6) as time_of_day,
                COUNT() as cnt
            FROM datarestorerapp_shopuseraction ds
            WHERE category_id = (
                SELECT id 
                FROM datarestorerapp_productcategory dp 
                WHERE dp.name = '{category}'
            )
            GROUP BY time_of_day
            ORDER BY COUNT(time_of_day) DESC
            """
        )
        return cursor.fetchall()


def get_max_number_of_requests_per_hour():
    """
    4. Какое максимальное число запросов на сайт за астрономический час
    (с 00 минут 00 секунд до 59 минут 59 секунд)?

    :return:
    """
    with sqlite3.connect(PATH_TO_DB) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                STRFTIME(SUBSTR(created_at, 0, 14)) as dtm,
                COUNT() as cnt
            FROM datarestorerapp_shopuseraction ds
            GROUP BY dtm
            ORDER BY COUNT(dtm) DESC LIMIT 1
            """
        )
        return cursor.fetchall()


def get_other_frequently_ordered_items():
    """
    5. Товары из какой категории чаще всего покупают совместно с товаром из
    категории “semi_manufactures”?

    :return:
    """
    with sqlite3.connect(PATH_TO_DB) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT 
                category_id, 
                COUNT() as cnt 
            FROM datarestorerapp_product dp3 
            WHERE id IN (
                SELECT 
                    product_id
                FROM datarestorerapp_orderitem do
                WHERE order_id in (
                    SELECT 
                        order_id 
                    FROM (
                        SELECT 
                            order_id 
                        FROM datarestorerapp_orderitem do 
                        WHERE product_id in (
                            SELECT 
                                id 
                            FROM datarestorerapp_product dp2 
                            WHERE category_id = (
                                SELECT 
                                    id 
                                FROM datarestorerapp_productcategory dp 
                                WHERE name = 'semi_manufactures'
                            )
                        )
                    )
                )
                AND product_id IN (
                    SELECT 
                        id 
                    FROM datarestorerapp_product dp2 
                    WHERE category_id IN (
                        SELECT 
                            id 
                        FROM datarestorerapp_productcategory dp 
                        WHERE name != 'semi_manufactures'
                    )
                )
                GROUP BY product_id
            )
            GROUP BY category_id
            ORDER BY cnt DESC
            """
        )
        return cursor.fetchall()


def get_unpaid_baskets_quantity() -> list:
    """
    6. Сколько не оплаченных корзин имеется?

    :return:
    """
    with sqlite3.connect(PATH_TO_DB) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT() as cnt 
            FROM datarestorerapp_order do 
            WHERE do.is_paid = 0
            """
        )

        return cursor.fetchall()


def get_regular_customer():
    """
    7. Какое количество пользователей совершали повторные покупки?

    :return:
    """
    with sqlite3.connect(PATH_TO_DB) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT()
            FROM (
                SELECT user_id
                FROM datarestorerapp_order do
                WHERE do.is_paid = 1
                GROUP BY user_id
                HAVING COUNT() > 1
            )
            """
        )

        return cursor.fetchall()


# print(*get_country_by_users(), sep='\n')
# print(*get_country_by_category(), sep='\n')
# print(*get_unpaid_baskets_quantity(), sep='\n')
# print(*get_regular_customer(), sep='\n')
# print(*get_time_of_day_by_category(), sep='\n')
# print(*get_max_number_of_requests_per_hour(), sep='\n')
# print(*get_other_frequently_ordered_items(), sep='\n')

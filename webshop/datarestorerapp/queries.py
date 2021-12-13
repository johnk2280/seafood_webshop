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
print(*get_regular_customer(), sep='\n')

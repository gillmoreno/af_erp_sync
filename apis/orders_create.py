import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql import query_sync_db
from _utils import get_meta_data_key
from orders_wp_apis import *


def create_new_orders_db_frontiera():
    new_orders = get_new_orders()
    for order in new_orders:
        shipping_address_id = get_shipping_address_id(order["shipping"])
        create_db_frontiera_order(
            id_wp=order["id"],
            currency=order["currency"],
            date_created=order["date_created"],
            discount_total=order["discount_total"],
            discount_tax=order["discount_tax"],
            shipping_total=order["shipping_total"],
            shipping_tax=order["shipping_tax"],
            cart_tax=order["cart_tax"],
            total=order["total"],
            total_tax=order["total_tax"],
            customer_id=order["customer_id"],
            shipping_address_id=shipping_address_id,
            customer_note=order["customer_note"],
            shipping_first_name=order["shipping"]["first_name"],
            shipping_last_name=order["shipping"]["last_name"],
            shipping_company=order["shipping"]["company"],
            shipping_address_1=order["shipping"]["address_1"],
            shipping_address_2=order["shipping"]["address_2"],
            shipping_city=order["shipping"]["city"],
            shipping_state=order["shipping"]["state"],
            shipping_postcode=order["shipping"]["postcode"],
            shipping_country=order["shipping"]["country"],
        )


def get_new_orders() -> list:
    db_frontiera_orders_wp_ids = get_db_frontiera_orders_wp_ids()
    ids_to_exclude = [_id[0] for _id in db_frontiera_orders_wp_ids]
    return get_orders(ids_to_exclude)


def get_shipping_address_id(shipping_address: dict) -> int:
    print(shipping_address)
    query = f"""
        SELECT
            id
        FROM
            shipping_addresses
        WHERE
            first_name='{shipping_address["first_name"]}' AND
            last_name='{shipping_address["last_name"]}' AND
            company='{shipping_address["company"]}' AND
            address_1='{shipping_address["address_1"]}' AND
            address_2='{shipping_address["address_2"]}' AND
            city='{shipping_address["city"]}' AND
            state_='{shipping_address["state"]}' AND
            postcode='{shipping_address["postcode"]}' AND
            country='{shipping_address["country"]}'
    """
    result = query_sync_db(query)
    return result[0][0] if result else 0


def create_db_frontiera_order(
    id_wp: int,
    currency: str,
    date_created: str,
    discount_total: float,
    discount_tax: float,
    shipping_total: float,
    shipping_tax: float,
    cart_tax: float,
    total: float,
    total_tax: float,
    customer_id: int,
    shipping_address_id: int,
    customer_note: str,
    shipping_first_name: str,
    shipping_last_name: str,
    shipping_company: str,
    shipping_address_1: str,
    shipping_address_2: str,
    shipping_city: str,
    shipping_state: str,
    shipping_postcode: str,
    shipping_country: str,
):
    query = f"""
        INSERT INTO 
            orders(
                id_wp,
                currency,
                date_created,
                discount_total,
                discount_tax,
                shipping_total,
                shipping_tax,
                cart_tax,
                total,
                total_tax,
                customer_id,
                shipping_address_id,
                customer_note,
                shipping_first_name,
                shipping_last_name,
                shipping_company,
                shipping_address_1,
                shipping_address_2,
                shipping_city,
                shipping_state,
                shipping_postcode,
                shipping_country
            ) 
        VALUES 
            (
                {id_wp},
                '{currency}',
                '{date_created}',
                {discount_total},
                {discount_tax},
                {shipping_total},
                {shipping_tax},
                {cart_tax},
                {total},
                {total_tax},
                {customer_id},
                {shipping_address_id},
                '{customer_note}',
                '{shipping_first_name}',
                '{shipping_last_name}',
                '{shipping_company}',
                '{shipping_address_1}',
                '{shipping_address_2}',
                '{shipping_city}',
                '{shipping_state}',
                '{shipping_postcode}',
                '{shipping_country}'
            ); 
    """
    query_sync_db(query, False, True)


def get_db_frontiera_orders_wp_ids():
    query = """
        SELECT
            id_wp
        FROM
            orders 
    """
    return query_sync_db(query)


if "__main__" in __name__:
    create_new_orders_db_frontiera()

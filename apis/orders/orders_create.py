import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db
from utils import *
from orders.orders_wp_apis import *
import json
import logging


@print_name
def create_new_orders_db_frontiera():
    """
    This cronjob must run AFTER customers sync
    """
    new_orders = get_new_orders()
    if not new_orders:
        logging.info("--> NO NEW ORDERS TO CREATE\n...\n")
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
        for item in order["line_items"]:
            create_db_frontiera_order_products(order["id"], item)


def get_new_orders() -> list:
    db_frontiera_orders_wp_ids = get_db_frontiera_orders_wp_ids()
    ids_to_exclude = [_id[0] for _id in db_frontiera_orders_wp_ids]
    return get_orders(ids_to_exclude)


def get_shipping_address_id(shipping_address: dict) -> int:
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
) -> None:
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


def create_db_frontiera_order_products(order_id: int, item: dict) -> None:
    cliche_position, uploaded_image, preview_image = get_cliche_info(item["meta_data"])
    query = f"""
        INSERT INTO
            order_products(
                order_id_wp,
                sku,
                quantity,
                subtotal,
                subtotal_tax,
                total,
                total_tax,
                price,
                uploaded_image,
                preview_image,
                cliche_position
            )
        VALUES
            (
                {order_id},
                '{item["sku"]}',
                {item["quantity"]},
                {item["subtotal"]},
                {item["subtotal_tax"]},
                {item["total"]},
                {item["total_tax"]},
                {item["price"]},
                '{uploaded_image}',
                '{preview_image}',
                '{cliche_position}'
            )

    """
    query_sync_db(query, False, True)


def get_cliche_info(meta_data: List[dict]) -> tuple:
    vpc_cart_data = get_meta_data_key(meta_data, "vpc-cart-data")
    vpc_custom_data = get_meta_data_key(meta_data, "vpc-custom-data")
    if vpc_cart_data != "NOT FOUND" and vpc_custom_data != "NOT FOUND":
        canvas_data = json.loads(vpc_cart_data["canvas_data"])
        keys = list(canvas_data["text_and_upload_panel"].keys())
        variable_key = keys[0] if keys else None
        uploaded_image = (
            canvas_data["text_and_upload_panel"][variable_key]["src"] if variable_key else ""
        )
        return (
            vpc_cart_data["Posizione clich??"],
            uploaded_image,
            vpc_custom_data["preview_saved"],
        )
    else:
        return "", "", ""


if "__main__" in __name__:
    create_new_orders_db_frontiera()

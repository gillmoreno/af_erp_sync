import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db
from utils import *
from orders.orders_wp_apis import *
import json
from loguru import logger


@print_name
def create_new_orders_db_frontiera():
    """
    Cronjob function
    Creates new order records in the local database for orders fetched from WordPress/WooCommerce.

    This function first retrieves new orders that have not yet been recorded in the local database.
    For each new order, it fetches or assigns a shipping address ID, creates a new order record in the
    database, and iterates through each line item in the order to create corresponding order product
    records, including detailed customization data like cliche colors and images.

    Note:
        This function must run after the customers synchronization process to ensure all relevant
        customer data is already present and updated in the database.
    """
    new_orders = get_new_orders()
    if not new_orders:
        logger.info("--> NO NEW ORDERS TO CREATE\n...\n")
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
    """
    Fetches a list of new orders from WordPress/WooCommerce that are not yet recorded in the local database.

    Returns:
        list: A list of new order data dictionaries, each representing an order to be created in the local database.
    """
    db_frontiera_orders_wp_ids = get_db_frontiera_orders_wp_ids()
    ids_to_exclude = [_id[0] for _id in db_frontiera_orders_wp_ids]
    return get_orders(ids_to_exclude)


def get_shipping_address_id(shipping_address: dict) -> int:
    """
    Retrieves the ID of a given shipping address from the local database, matching by address details.

    Args:
        shipping_address (dict): A dictionary containing the details of the shipping address.

    Returns:
        int: The ID of the shipping address in the local database, or 0 if not found.
    """
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
    """
    Creates a new order record in the local database with detailed order and shipping information.

    Args:
        id_wp (int): WordPress ID of the order.
        currency (str): Currency code for the order totals.
        date_created (str): Creation date of the order.
        discount_total, discount_tax, shipping_total, shipping_tax, cart_tax, total, total_tax (float): Financial totals for the order.
        customer_id (int): ID of the customer placing the order.
        shipping_address_id (int): ID of the shipping address associated with the order.
        customer_note (str): Note left by the customer with the order.
        shipping_first_name, shipping_last_name, shipping_company, shipping_address_1, shipping_address_2, shipping_city, shipping_state, shipping_postcode, shipping_country (str): Details of the shipping address.

    Creates a detailed order record in the `orders` table of the local database, including financial totals, customer and shipping information.
    """
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
    """
    Retrieves WordPress IDs for all orders currently recorded in the local database.

    Returns:
        A list of WordPress order IDs (id_wp) from the `orders` table in the local database.
    """
    query = """
        SELECT
            id_wp
        FROM
            orders 
    """
    return query_sync_db(query)


def create_db_frontiera_order_products(order_id: int, item: dict) -> None:
    """
    Creates records for each product in an order, including customization details like cliche colors and images.

    Args:
        order_id (int): The local database ID of the order to which the product belongs.
        item (dict): A dictionary containing details of the order item, including SKU, quantity, pricing, and customization metadata.

    Inserts a record for each product in the `order_products` table of the local database, capturing detailed product information and customizations.
    """
    # TODO add notes custom field also here, product metadata (product_notes)
    # print(item)
    # item["meta_data"]["product_notes"]
    # TODO add notes from configurator also here (from cliche_info)
    # TODO add 2 extra columns to order_products in db_forntiera
    cliche_color_inside, cliche_color_outside, uploaded_image_inside, uploaded_image_outside, preview_image = (
        get_cliche_info(item["meta_data"])
    )
    # cliche_color_inside, cliche_color_outside, uploaded_image_inside, uploaded_image_outside, preview_image, cliche_note = get_cliche_info(item["meta_data"])
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
                uploaded_image_inside,
                uploaded_image_outside,
                preview_image,
                cliche_color_inside,
                cliche_color_outside
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
                '{uploaded_image_inside}',
                '{uploaded_image_outside}',
                '{preview_image}',
                '{cliche_color_inside}',
                '{cliche_color_outside}'
            )

    """
    query_sync_db(query, False, True)


def get_cliche_info(meta_data: List[dict]) -> tuple:
    """
    Extracts cliche customization information from order product metadata.

    Args:
        meta_data (List[dict]): A list of metadata dictionaries associated with an order product.

    Returns:
        tuple: Contains cliche color information for the interior and exterior, uploaded images for inside and outside, and a preview image URL.
    """
    vpc_cart_data = get_meta_data_key(meta_data, "vpc-cart-data")
    vpc_custom_data = get_meta_data_key(meta_data, "vpc-custom-data")
    if vpc_cart_data != "NOT FOUND" and vpc_custom_data != "NOT FOUND":
        canvas_data = json.loads(vpc_cart_data["canvas_data"])
        keys = list(canvas_data["text_and_upload_panel_0"].keys())
        variable_key = keys[0] if keys else None
        uploaded_image_inside = canvas_data["text_and_upload_panel_0"][variable_key]["src"] if variable_key else ""
        keys = list(canvas_data["text_and_upload_panel_1"].keys())
        variable_key = keys[0] if keys else None
        uploaded_image_outside = canvas_data["text_and_upload_panel_1"][variable_key]["src"] if variable_key else ""
        if "Colore per l'interno" in vpc_cart_data:
            cliche_color_inside = vpc_cart_data["Colore per l'interno"]
        if "Color for the interior" in vpc_cart_data:
            cliche_color_inside = vpc_cart_data["Color for the interior"]
        if "Colore per il fronte" in vpc_cart_data:
            cliche_color_inside = vpc_cart_data["Colore per il fronte"]
        if "Color for the front" in vpc_cart_data:
            cliche_color_inside = vpc_cart_data["Color for the front"]

        if "Colore per l'esterno" in vpc_cart_data:
            cliche_color_outside = vpc_cart_data["Colore per l'esterno"]
        if "Color for the exterior" in vpc_cart_data:
            cliche_color_outside = vpc_cart_data["Color for the exterior"]
        if "Colore per il retro" in vpc_cart_data:
            cliche_color_outside = vpc_cart_data["Colore per il retro"]
        if "Color for the back" in vpc_cart_data:
            cliche_color_outside = vpc_cart_data["Color for the back"]

        # TODO
        # if "Cliche note" in vpc_cart_data:
        #     cliche_note = vpc_cart_data["Cliche note"]

        # print(vpc_cart_data) to find the notes
        # vpc_cart_data["notes... despcription"]
        # return at the end

        return (
            # vpc_cart_data["Colore"],
            cliche_color_inside,
            cliche_color_outside,
            uploaded_image_inside,
            uploaded_image_outside,
            vpc_custom_data["preview_saved"],
            # cliche_note,
        )
    else:
        return "", "", "", "", ""
        # return "", "", "", "", "", ""


if "__main__" in __name__:
    create_new_orders_db_frontiera()

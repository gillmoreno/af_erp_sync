import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db
from utils import *
from customers.customers_wp_apis import *
from customers.customers__common import *


@print_name
def update_customers_db_frontiera():
    existing_customers = get_existing_customers()
    for customer in existing_customers:
        update_db_frontiera_customer(
            customer["id"],
            get_meta_data_key(customer["meta_data"], "pw_user_status"),
            customer["email"],
            customer["username"],
            customer["first_name"],
            customer["last_name"],
        )
        update_db_frontiera_billing_address(
            customer["id"],
            customer["billing"]["first_name"],
            customer["billing"]["last_name"],
            customer["billing"]["company"],
            customer["billing"]["address_1"],
            customer["billing"]["address_2"],
            customer["billing"]["city"],
            customer["billing"]["state"],
            customer["billing"]["postcode"],
            customer["billing"]["country"],
            customer["billing"]["email"],
            customer["billing"]["phone"],
        )
        multiple_shipping_addresses = get_multiple_shipping_addresses(customer["meta_data"])
        if multiple_shipping_addresses:
            update_db_frontiera_shipping_addresses(customer["id"], multiple_shipping_addresses)
        else:
            update_db_frontiera_default_shipping_address(
                customer["id"],
                customer["shipping"]["first_name"],
                customer["shipping"]["last_name"],
                customer["shipping"]["company"],
                customer["shipping"]["address_1"],
                customer["shipping"]["address_2"],
                customer["shipping"]["city"],
                customer["shipping"]["state"],
                customer["shipping"]["postcode"],
                customer["shipping"]["country"],
            )


def get_existing_customers() -> list:
    db_frontiera_users_wp_ids = get_db_frontiera_users_wp_ids()
    ids_to_include = [_id[0] for _id in db_frontiera_users_wp_ids]
    return get_customers(ids_to_include, True)


def update_db_frontiera_customer(
    id_wp: int,
    pw_user_status: str,
    email: str,
    username: str,
    first_name: str,
    last_name: str,
):
    query = f"""
        UPDATE 
            customers 
        SET
            pw_user_status='{pw_user_status}',
            email='{email}',
            username='{username}',
            first_name='{first_name}',
            last_name='{last_name}'
        WHERE
            id_wp={str(id_wp)};
    """
    query_sync_db(query, False, True)


def update_db_frontiera_billing_address(
    id_wp: int,
    first_name: str,
    last_name: str,
    company: str,
    address_1: str,
    address_2: str,
    city: str,
    state_: str,
    postcode: str,
    country: str,
    email: str,
    phone: str,
):
    query = f"""
        UPDATE
            billing_addresses
        SET
            first_name='{first_name}',
            last_name='{last_name}',
            company='{company}',
            address_1='{address_1}',
            address_2='{address_2}',
            city='{city}',
            state_='{state_}',
            postcode='{postcode}',
            country='{country}',
            email='{email}',
            phone='{phone}'
        WHERE
            id_wp_customer={str(id_wp)};
    """
    query_sync_db(query, False, True)


def update_db_frontiera_default_shipping_address(
    id_wp: int,
    first_name: str,
    last_name: str,
    company: str,
    address_1: str,
    address_2: str,
    city: str,
    state_: str,
    postcode: str,
    country: str,
):
    query = f"""
        SELECT
            shipping_address_id
        FROM
            customers_shipping_addresses
        WHERE
            customer_id={str(id_wp)}
    """
    shipping_address_id = query_sync_db(query, True)[0]["shipping_address_id"]
    query = f"""
        UPDATE
            shipping_addresses
        SET
            first_name='{first_name}',
            last_name='{last_name}',
            company='{company}',
            address_1='{address_1}',
            address_2='{address_2}',
            city='{city}',
            state_='{state_}',
            postcode='{postcode}',
            country='{country}'
        WHERE
            id={str(shipping_address_id)};
    """
    query_sync_db(query, False, True)


def get_multiple_shipping_addresses(meta_data: list):
    for item in meta_data:
        if item["key"] == "thwma_custom_address":
            return item["value"]
    return False


def update_db_frontiera_shipping_addresses(wp_customer_id: int, thwma_custom_address: dict) -> None:
    for address in thwma_custom_address["shipping"].keys():
        query = f"""
            SELECT
                shipping_address_id
            FROM
                customers_shipping_addresses
            WHERE
                customer_id={str(wp_customer_id)} and address_book='{address}'
        """
        shipping_address = query_sync_db(query, True)
        if shipping_address and "shipping_address_id" in shipping_address[0].keys():
            query = f"""
                UPDATE
                    shipping_addresses
                SET
                    first_name='{thwma_custom_address["shipping"][address].get("shipping_first_name", "")}',
                    last_name='{thwma_custom_address["shipping"][address].get("shipping_last_name", "")}',
                    company='{thwma_custom_address["shipping"][address].get("shipping_company", "")}',
                    address_1='{thwma_custom_address["shipping"][address].get("shipping_address_1", "")}',
                    address_2='{thwma_custom_address["shipping"][address].get("shipping_address_2", "")}',
                    city='{thwma_custom_address["shipping"][address].get("shipping_city", "")}',
                    state_='{thwma_custom_address["shipping"][address].get("shipping_state", "")}',
                    postcode='{thwma_custom_address["shipping"][address].get("shipping_postcode", "")}',
                    country='{thwma_custom_address["shipping"][address].get("shipping_country", "")}'
                WHERE
                    id={str(shipping_address[0]["shipping_address_id"])};
            """
            query_sync_db(query, False, True)
        else:
            query = f"""
                INSERT INTO 
                    shipping_addresses(
                        first_name,
                        last_name,
                        company,
                        address_1,
                        address_2,
                        city,
                        state_,
                        postcode,
                        country
                    ) 
                VALUES 
                    (
                        '{thwma_custom_address["shipping"][address].get("shipping_first_name", "")}',
                        '{thwma_custom_address["shipping"][address].get("shipping_last_name", "")}',
                        '{thwma_custom_address["shipping"][address].get("shipping_company", "")}',
                        '{thwma_custom_address["shipping"][address].get("shipping_address_1", "")}',
                        '{thwma_custom_address["shipping"][address].get("shipping_address_2", "")}',
                        '{thwma_custom_address["shipping"][address].get("shipping_city", "")}',
                        '{thwma_custom_address["shipping"][address].get("shipping_state", "")}',
                        '{thwma_custom_address["shipping"][address].get("shipping_postcode", "")}',
                        '{thwma_custom_address["shipping"][address].get("shipping_country", "")}'
                    ); 
            """
            shipping_address_id = query_sync_db(query, True, True)
            query = f"""
                INSERT INTO
                    customers_shipping_addresses(
                        shipping_address_id,
                        customer_id,
                        address_book
                    )
                VALUES
                    (
                        {shipping_address_id},
                        {wp_customer_id},
                        '{address}'
                    )
            """
            query_sync_db(query, False, True)


if "__main__" in __name__:
    update_customers_db_frontiera()

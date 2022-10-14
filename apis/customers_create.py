import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql import query_sync_db
from typing import List
from customers_wp_apis import *


def create_new_customers_db_frontiera():
    new_customers = get_new_approved_customers()
    for customer in new_customers:
        create_db_frontiera_customer(
            customer["id"],
            get_meta_data_key(customer["meta_data"], "pw_user_status"),
            customer["email"],
            customer["username"],
            customer["first_name"],
            customer["last_name"],
            get_meta_data_key(customer["meta_data"], "vat_number"),
        )
        create_db_frontiera_addresses(
            customer["id"],
            customer["billing"]["company"],
            customer["billing"]["country"],
        )


def get_new_approved_customers() -> list:
    db_frontiera_users_wp_ids = get_db_frontiera_users_wp_ids()
    ids_to_exclude = [_id[0] for _id in db_frontiera_users_wp_ids]
    return get_customers(ids_to_exclude)


def create_db_frontiera_customer(
    id_wp: int,
    pw_user_status: str,
    email: str,
    username: str,
    first_name: str,
    last_name: str,
    vat_number: str,
):
    query = f"""
        INSERT INTO 
            customers(
                id_wp,
                pw_user_status,
                email,
                username,
                first_name,
                last_name,
                vat_number,
                wp_needs_sync,
                sam_erp_needs_sync
            ) 
        VALUES 
            (
                {id_wp},
                '{pw_user_status}',
                '{email}',
                '{username}',
                '{first_name}',
                '{last_name}',
                '{vat_number}',
                0,
                0
            ); 
    """
    query_sync_db(query, False, True)


def get_db_frontiera_users_wp_ids():
    query = """
        SELECT
            id_wp
        FROM
            customers
    """
    return query_sync_db(query)


def get_meta_data_key(meta_data: List[dict], key) -> str:
    for data in meta_data:
        if data["key"] == key:
            return data["value"]
    return "NOT FOUND"


def create_db_frontiera_addresses(
    id_wp: int,
    company: str,
    country: str,
):
    query = f"""
        INSERT INTO 
            billing_addresses(
                id_wp_customer,
                company,
                country
            ) 
        VALUES 
            (
                {id_wp},
                '{company}',
                '{country}'
            ); 
    """
    query_sync_db(query, False, True)
    query = f"""
        INSERT INTO 
            shipping_addresses(
                company,
                country
            ) 
        VALUES 
            (
                '{company}',
                '{country}'
            ); 
    """
    shipping_address_id = query_sync_db(query, False, True)
    query = f"""
        INSERT INTO 
            customers_shipping_addresses(
                shipping_address_id,
                customer_id
            ) 
        VALUES 
            (
                {shipping_address_id},
                {id_wp}
            ); 
    """
    query_sync_db(query, False, True)


if "__main__" in __name__:
    create_new_customers_db_frontiera()

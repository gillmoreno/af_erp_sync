"""
Facilitates the creation of new customer records in the local database based on data from WordPress.

This module identifies new customers from WordPress that are not yet recorded in the local database
(`db_frontiera`) and creates corresponding records, ensuring the local customer data is synchronized
with WordPress.
"""

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db
from utils import *
from customers.customers_wp_apis import *
from customers.customers__common import *
from loguru import logger


@print_name
def create_new_customers_db_frontiera():
    """
    Identifies new customers from WordPress not present in the local database and creates records for them.

    This function fetches customer data from WordPress, checks against the local database to identify
    new customers, and creates records in the local database for these new customers. It handles the
    synchronization of basic customer information as well as their addresses.

    Side Effects:
        - Logs information about the synchronization process.
        - Updates the local database with new customer records, including basic information and addresses.
    """
    new_customers = get_new_customers()
    if not new_customers:
        logger.info("--> NO NEW CUSTOMERS TO SYNC\n...\n")
    for customer in new_customers:
        create_db_frontiera_customer(
            customer["id"],
            get_meta_data_key(customer["meta_data"], "pw_user_status"),
            customer["email"],
            customer["username"],
            customer["first_name"],
            customer["last_name"],
            get_meta_data_key(customer["meta_data"], "vat_number"),
            get_meta_data_key(customer["meta_data"], "pec"),
            get_meta_data_key(customer["meta_data"], "codice_fiscale"),
            get_meta_data_key(customer["meta_data"], "sdi_code"),
        )
        create_db_frontiera_addresses(
            customer["id"],
            customer["billing"]["company"],
            customer["billing"]["country"],
        )


def get_new_customers() -> list:
    """
    Retrieves a list of new customers from WordPress that are not yet recorded in the local database.

    This function fetches WordPress customer IDs, filters out those already present in the local database,
    and returns a list of customers to be synchronized.

    Returns:
        list: A list of customer data dictionaries for customers that need to be added to the local database.
    """
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
    pec: str = "",
    cf: str = "",
    sdi_code: str = "",
):
    """
    Creates a new customer record in the local database with details fetched from WordPress.

    Args:
        id_wp (int): The WordPress ID of the customer.
        pw_user_status (str): The status of the user in the WordPress site.
        email (str): The email address of the customer.
        username (str): The username of the customer.
        first_name (str): The first name of the customer.
        last_name (str): The last name of the customer.
        vat_number (str): The VAT number of the customer.

    Creates a record in the `customers` table of the local database with the provided customer details.
    """
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


def create_db_frontiera_addresses(
    id_wp: int,
    company: str,
    country: str,
):
    """
    Creates billing and shipping address records in the local database for a given customer.

    Args:
        id_wp (int): The WordPress ID of the customer, used to link the address records.
        company (str): The company name associated with the customer's billing and shipping addresses.
        country (str): The country associated with the customer's billing and shipping addresses.

    Creates records in both `billing_addresses` and `shipping_addresses` tables, and links the shipping
    address to the customer in the `customers_shipping_addresses` table.
    """
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

"""
Facilitates the update of existing customer records in the local database with data from WordPress.

This module fetches the latest customer information from WordPress and updates the corresponding
records in the local database (`db_frontiera`), ensuring that customer data remains synchronized
between the two systems.
"""

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db
from utils import *
from customers.customers_wp_apis import *
from customers.customers__common import *


@print_name
def update_customers_db_frontiera():
    """
    Updates existing customer records in the local database with the latest information from WordPress.

    Fetches existing customer data from WordPress, identifies corresponding records in the local database,
    and updates these records with the latest available information, including user status, email, username,
    and names.

    Side Effects:
        - Logs the name of the function being executed for tracking purposes.
        - Performs database update operations to synchronize customer data.
    """
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
    """
    Retrieves a list of existing customers from the local database who have corresponding records in WordPress.

    This function is designed to fetch customer records that already exist in the local database and may require
    updates to synchronize with the latest data available in WordPress.

    Returns:
        A list of dictionaries, where each dictionary represents an existing customer record including essential
        fields such as customer ID, meta data, email, username, and names necessary for the update process.
    """
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
    """
    Updates a single customer record in the local database with new data.

    Args:
        id_wp (int): WordPress ID of the customer.
        pw_user_status (str): Current status of the customer in WordPress.
        email (str): Customer's email address.
        username (str): Customer's username.
        first_name (str): Customer's first name.
        last_name (str): Customer's last name.

    Updates the specified customer's record in the `customers` table of the local database with the provided details.
    """
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
    """
    Updates the billing address for a given customer in the local database.

    Args:
        id_wp (int): WordPress ID of the customer whose billing address is to be updated.
        first_name (str), last_name (str), company (str), address_1 (str), address_2 (str), city (str): Components of the billing address.

    Updates the billing address details for the specified customer in the local database, ensuring that the information matches the latest data from WordPress.
    """
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
    """
    Updates the default shipping address for a specified WordPress customer in the local database.

    Args:
        id_wp (int): WordPress ID of the customer.
        first_name (str): First name for the shipping address.
        last_name (str): Last name for the shipping address.
        company (str): Company name for the shipping address.
        address_1 (str): Primary address line.
        address_2 (str): Secondary address line (optional).
        city (str): City of the shipping address.
        state_ (str): State or region of the shipping address.
        postcode (str): Postal code of the shipping address.
        country (str): Country of the shipping address.

    Fetches the current default shipping address ID for the customer, then updates the address details in the
    `shipping_addresses` table based on the provided information.
    """
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
    """
    Extracts multiple shipping addresses from the provided meta_data if available.

    Args:
        meta_data (list): A list of meta data items from which to extract multiple shipping addresses.

    Returns:
        The value associated with the "thwma_custom_address" key if it exists, indicating the presence of
        multiple custom shipping addresses; otherwise, returns False.
    """
    for item in meta_data:
        if item["key"] == "thwma_custom_address":
            return item["value"]
    return False


def update_db_frontiera_shipping_addresses(wp_customer_id: int, thwma_custom_address: dict) -> None:
    """
    Updates or inserts multiple shipping addresses for a specific WordPress customer in the local database.

    Args:
        wp_customer_id (int): WordPress ID of the customer whose shipping addresses are being updated.
        thwma_custom_address (dict): A dictionary containing the 'shipping' key with nested dictionaries
                                     for each address, keyed by a unique identifier and containing address details.

    For each address in the `thwma_custom_address` dictionary, this function either updates an existing
    shipping address record in the `shipping_addresses` table if it exists or inserts a new record if it does not.
    It also ensures that each shipping address is linked to the customer in the `customers_shipping_addresses` table.
    """
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

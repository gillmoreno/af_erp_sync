import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql import query_sync_db
from typing import List
from customers import *


# customers_with_no_address_ids = get_customers_with_no_addresses_from_db_frontiera()
# get_customers(customers_with_no_address_ids, True)


def sync_addresses_with_db_frontiera():
    customers = get_customers()
    for customer in customers:
        print(customer["billing"])


def construct_update_billing_address_query(billing_data: dict) -> None:
    return """
        UPDATE
            billing_addresses
        SET
            id_wp_customer
            first_name
            last_name
            company
            address_1
            address_2
            city
            state_
            post_code
            country
            email
            phone
        WHERE

    """


sync_addresses_with_db_frontiera()

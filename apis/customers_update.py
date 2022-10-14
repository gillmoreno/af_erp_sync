import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql import query_sync_db
from _utils import get_meta_data_key
from customers_wp_apis import *
from customers__common import *


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
        update_db_frontiera_billing_addresses(
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
        # update_db_frontiera_shipping_addresses(
        #     customer["shipping"]["first_name"],
        #     customer["shipping"]["last_name"],
        #     customer["shipping"]["company"],
        #     customer["shipping"]["address_1"],
        #     customer["shipping"]["address_2"],
        #     customer["shipping"]["city"],
        #     customer["shipping"]["state"],
        #     customer["shipping"]["postcode"],
        #     customer["shipping"]["country"],
        # )


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


def update_db_frontiera_billing_addresses(
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


# def update_db_frontiera_shipping_addresses(
#     first_name: str,
#     last_name: str,
#     company: str,
#     address_1: str,
#     address_2: str,
#     city: str,
#     state_: str,
#     postcode: str,
#     country: str,
# ):
#     query = f"""
#         UPDATE
#             customers
#         SET
#             first_name='{first_name}',
#             last_name='{last_name}',
#             company='{company}',
#             address_1='{address_1}',
#             address_2='{address_2}',
#             city='{city}',
#             state_='{state_}',
#             postcode='{postcode}',
#             country='{country}'
#         WHERE
#             id_wp={str(id_wp)};
#     """
#     query_sync_db(query, False, True)


if "__main__" in __name__:
    update_customers_db_frontiera()

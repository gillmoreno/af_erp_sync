import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql import query_sync_db
from customers_wp_apis import *


def sync_wp_user_status():
    wp_users_to_sync = get_wp_users_to_sync()
    for user in wp_users_to_sync:
        update_customer_status(user["id_wp"], user["pw_user_status"])
        update_wp_needs_sync(user["id_wp"])


def get_wp_users_to_sync():
    query = """
        SELECT
            id_wp,
            pw_user_status
        FROM
            customers
        WHERE
            wp_needs_sync = 1;
    """
    return query_sync_db(query, True)


def update_wp_needs_sync(id_wp: int) -> None:
    query = f"""
        UPDATE
            customers
        SET
            wp_needs_sync=0
        WHERE
            id_wp = {str(id_wp)};
    """
    print(query)
    query_sync_db(query, False, True)


if "__main__" in __name__:
    sync_wp_user_status()

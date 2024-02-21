"""
Contains common utility functions used in the customer-related parts of the API.

This module provides functionalities that support operations involving the synchronization
and management of customer data between an external system and WordPress.
"""

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db


def get_db_frontiera_users_wp_ids():
    """
    Retrieves WordPress IDs for all customers from the database.

    This function executes a SQL query against the `customers` table to collect the WordPress
    IDs (id_wp) associated with each customer record.

    Returns:
        A list of dictionaries, each containing the 'id_wp' of a customer.
    """
    query = """
        SELECT
            id_wp
        FROM
            customers
    """
    return query_sync_db(query)

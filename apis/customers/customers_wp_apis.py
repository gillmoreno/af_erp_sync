from typing import List
from dotenv import load_dotenv
import requests
from loguru import logger
from apis.sql import query_sync_db
from apis.auth import wcapi
import os
import sys


def update_customer_status(id_wp: int, status: str):
    """
    Updates the status of a specified customer in WordPress.

    Args:
        id_wp (int): The WordPress ID of the customer to update.
        status (str): The new status to assign to the customer.

    Logs the operation and sends a PUT request to the WooCommerce REST API to update the customer's status
    by modifying the "pw_user_status" meta data field.
    """
    logger.info(f"-> update_customer_status id_wp: {str(id_wp)}, status: {status}")
    data = {
        "meta_data": [
            {
                "key": "pw_user_status",
                "value": status,
            },
        ]
    }
    logger.info(wcapi.put(f"customers/{str(id_wp)}", data).json())


def retrieve_customer(customer_id: int):
    """
    Retrieves detailed information for a specific customer from WordPress.

    Args:
        customer_id (int): The WordPress ID of the customer to retrieve.

    Returns:
        dict: A dictionary containing the detailed information of the customer as returned by the WooCommerce REST API.
    """
    return wcapi.get(f"customers/{str(customer_id)}").json()


def get_customers(ids: List[int] = [], include: bool = False):
    """
    Retrieves a list of customers from WordPress, optionally filtering by inclusion or exclusion of specific IDs.

    Args:
        ids (List[int]): A list of customer IDs to either include or exclude from the results.
        include (bool): Determines whether the provided IDs should be included or excluded in the results. Defaults to False (exclude).

    Returns:
        list: A list of customers as returned by the WooCommerce REST API, based on the inclusion or exclusion filter.
    """
    ids_string = ",".join(str(_id) for _id in ids)
    filter_ = "include" if include else "exclude"
    return wcapi.get(f"customers?{filter_}={ids_string}").json()


def delete_customer(customer_id: int):
    """
    Permanently deletes a specified customer from WordPress.

    Args:
        customer_id (int): The WordPress ID of the customer to delete.

    Returns:
        dict: A dictionary containing the response from the WooCommerce REST API regarding the deletion operation.

    Note:
        This operation is irreversible and will permanently remove the customer's record from WordPress.
    """
    return wcapi.delete(f"customers/{str(customer_id)}", params={"force": True}).json()

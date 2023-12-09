from typing import List
from dotenv import load_dotenv
import requests
from loguru import logger
from apis.sql import query_sync_db
from apis.auth import wcapi
import os
import sys


def update_customer_status(id_wp: int, status: str):
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
    return wcapi.get(f"customers/{str(customer_id)}").json()


def get_customers(ids: List[int] = [], include: bool = False):
    ids_string = ",".join(str(_id) for _id in ids)
    filter_ = "include" if include else "exclude"
    return wcapi.get(f"customers?{filter_}={ids_string}").json()


def delete_customer(customer_id: int):
    return wcapi.delete(f"customers/{str(customer_id)}", params={"force": True}).json()

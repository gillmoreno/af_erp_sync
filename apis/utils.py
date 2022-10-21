from typing import List
import logging


def get_meta_data_key(meta_data: List[dict], key) -> str:
    for data in meta_data:
        if data["key"] == key:
            return data["value"]
    return "NOT FOUND"


def print_name(func):
    def wrapper():
        logging.info(f"--> START executing {func.__name__}")
        func()
        logging.info(f"--> FINISHED executing {func.__name__}\n ...")

    return wrapper

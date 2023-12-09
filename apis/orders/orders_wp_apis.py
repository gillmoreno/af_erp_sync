from auth import wcapi
from typing import List


def all_orders() -> List[dict]:
    return wcapi.get("orders").json()


def get_orders(ids: List[int] = [], include: bool = False):
    ids_string = ",".join(str(_id) for _id in ids)
    filter_ = "include" if include else "exclude"
    return wcapi.get(f"orders?{filter_}={ids_string}").json()


def copy_order(order_id: int):
    
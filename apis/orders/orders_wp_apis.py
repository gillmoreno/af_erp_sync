from auth import wcapi
from typing import List


def all_orders() -> List[dict]:
    """
    Fetches all orders from the WooCommerce API.

    Returns:
        List[dict]: A list of dictionaries where each dictionary represents an order.
    """
    return wcapi.get("orders").json()


def get_orders(ids: List[int] = [], include: bool = False):
    """
    Fetches orders from the WooCommerce API based on the provided IDs.

    Args:
        ids (List[int], optional): A list of order IDs to include or exclude. Defaults to [].
        include (bool, optional): If True, only the orders with the provided IDs are fetched.
                                   If False, all orders except those with the provided IDs are fetched.
                                   Defaults to False.

    Returns:
        List[dict]: A list of dictionaries where each dictionary represents an order.
    """
    ids_string = ",".join(str(_id) for _id in ids)
    filter_ = "include" if include else "exclude"
    return wcapi.get(f"orders?{filter_}={ids_string}").json()

from auth import wcapi
from typing import List


def all_orders() -> List[dict]:
    return wcapi.get("orders").json()


def get_orders(ids: List[int] = [], include: bool = False):
    ids_string = ",".join(str(_id) for _id in ids)
    filter_ = "include" if include else "exclude"
    return wcapi.get(f"orders?{filter_}={ids_string}").json()


if "__main__" in __name__:
    orders = all_orders()

    for k, i in orders[1].items():
        print({k: i})
    # for item in orders[1]["line_items"][0]["meta_data"]:
    #     for k, i in item.items():
    #         print({k: i})

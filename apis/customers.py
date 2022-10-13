from auth import wcapi
from typing import List


def update_customer_status(id_wp: int, status: str):
    data = {
        "meta_data": [
            {
                "key": "pw_user_status",
                "value": status,
            },
        ]
    }
    print(wcapi.put(f"customers/{str(id_wp)}", data).json())


def retrieve_customer(customer_id: int):
    return wcapi.get(f"customers/{str(customer_id)}").json()


def get_customers(exclude_ids: List[int] = []):
    exclude_ids_string = ",".join(str(_id) for _id in exclude_ids)
    return wcapi.get(f"customers?exclude={exclude_ids_string}").json()


def delete_customer(customer_id: int):
    return wcapi.delete(f"customers/{str(customer_id)}", params={"force": True}).json()


from auth import wcapi

def create_customer(
        email: str,
        first_name: str,
        last_name: str,
        username: str,
        billing: dict = {},
        shipping: dict = {}
    ):
    data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "billing": billing,
        "shipping": shipping,
    }
    print(wcapi.post("customers", data).json())

def retrieve_customer(customer_id: int):
    return wcapi.get(f"customers/{str(customer_id)}").json()

def all_customers():
    return wcapi.get("customers").json()

def delete_customer(customer_id: int):
    return wcapi.delete(f"customers/{str(customer_id)}", params={"force": True}).json()

# create_customer(
#     email="biv@hotmail.com",
#     first_name="biv",
#     last_name="oc",
#     username="bivoc",
# )

print(delete_customer(4))
print(all_customers())
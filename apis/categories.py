
from auth import wcapi

categories = wcapi.get("products/categories").json()

for category in categories:
    print("####------####")
    print(category)
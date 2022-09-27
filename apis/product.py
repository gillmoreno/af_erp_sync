# https://woocommerce.github.io/woocommerce-rest-api-docs/?python#product-properties

from .auth import wcapi

def create_product(
        name: str,
        _type: str,
        regular_price: str,
        description_it: str,
        short_description_it: str,
        description_en: str,
        short_description_en: str,
        categories: list, #list of dicts
        images: list,
        dimensions: dict,
        meta: dict = {}
    ):
    data = {
        "name": name,
        "type": _type,
        "regular_price": regular_price,
        "description_it": description_it,
        "short_description_it": short_description_it,
        "description_en": description_en,
        "short_description_en": short_description_en,
        "categories": categories,
        "images": images,
        "dimensions": dimensions,
        "meta": meta
    }
    print(wcapi.post("products", data).json())

def retrieve_product(product_id: int):
    print(wcapi.get(f"products/{str(product_id)}").json())

def update_product(product_id: int, data: dict):
    print(wcapi.put(f"products/{str(product_id)}", data).json())

def delete_product(product_id: int):
    print(wcapi.delete(f"products/{str(product_id)}", params={"force": True}).json())

# create_product(
#     name="Will it work with dimensions?",
#     _type="variable",
#     regular_price='12',
#     description_it="La descrizione in italiano",
#     short_description_it="Desc ita",
#     description_en="The description in english",
#     short_description_en="Desc eng",
#     categories=[{'id': 27}],
#     dimensions={
#         'length': '10',
#         'width': '10',
#         'height': '10'
#     },
#     images=""
# )



# print(len(wcapi.get("products").json()))
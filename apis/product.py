# https://woocommerce.github.io/woocommerce-rest-api-docs/?python#product-properties

from auth import wcapi

def create_product(
        title_it: str,
        title_en: str,
        _type: str,
        # regular_price: str,
        description_it: str,
        description_en: str,
        short_description_it: str,
        short_description_en: str,
        categories: list, #list of dicts
        images: list,
        # dimensions: dict,
        attributes: list,
        meta_it: list = [],
        meta_en: list = [],
    ) -> int:
    data = {
        "name": title_it,
        "type": _type,
        # "regular_price": regular_price,
        "description": description_it,
        "short_description": short_description_it,
        "categories": categories,
        "images": images,
        # "dimensions": dimensions,
        "attributes": attributes,
        "meta_data": meta_it
    }
    italian_product = wcapi.post("products", data).json()
    data_en = {
        "name": title_en,
        "description": description_en,
        "short_description": short_description_en,
        "meta_data": meta_en,
        "lang": "en",
        "translation_of": italian_product['id']
    }
    print(wcapi.post("products", data_en).json())
    return italian_product['id']


def retrieve_product(product_id: int):
    print(wcapi.get(f"products/{str(product_id)}").json())

def update_product(product_id: int, data: dict):
    print(wcapi.put(f"products/{str(product_id)}", data).json())

def delete_product(product_id: int):
    print(wcapi.delete(f"products/{str(product_id)}", params={"force": True}).json())

def create_product_variation(
        product_id: int,
        sku: str,
        regular_price: str,
        image: dict,
        dimensions: dict,
        attributes_it: list,
        attributes_en: list,
    ) -> int:
    """Attributes must be created beforehand"""
    data = {
        "sku": sku,
        "regular_price": regular_price,
        "image": image,
        "dimensions": dimensions,
        "attributes": attributes_it
    }
    italian_variation = wcapi.post(f"products/{str(product_id)}/variations", data).json()
    print(italian_variation)
    data_en = {
        "lang": "en",
        "translation_of": italian_variation['id'],
        "attributes": attributes_en
    }
    print(wcapi.post(f"products/{str(product_id+1)}/variations", data_en).json())
    return italian_variation['id']


# create_product(
#     name_it="Python + REST API",
#     name_en="Oh YEAH!",
#     _type="variable",
#     regular_price='12',
#     description_it="La descrizione in italiano",
#     short_description_it="Desc ita",
#     description_en="ENGLISH STUFF",
#     short_description_en="EN...",
#     categories=[{'id': 42}],
#     dimensions={
#         'length': '15',
#         'width': '15',
#         'height': '15'
#     },
#     attributes=[
#         {
#             "id": 2,
#             "variation": True,
#             "visible": True,
#             "options": ["100x100", "200x200"]
#         },
#         {
#             "id": 3,
#             "variation": True,
#             "visible": True,
#             "options": ["Rosso - Rosso", "Viola - Blu"]
#         },
#     ],
#     images="",
#     meta_it = [
#         {
#             "key": "_yoast_wpseo_metadesc",
#             "value": "Prova SEO"
#         }
#     ],
#     meta_en = [
#         {
#             "key": "_yoast_wpseo_metadesc",
#             "value": "Some SEO Test"
#         }
#     ]
# )


# create_product_variation(
#     product_id=212,
#     sku="sku_05",
#     regular_price="199",
#     image=None,
#     dimensions={
#         'length': '25',
#         'width': '100',
#         'height': '333'
#     },
#     attributes_it=[
#         {
#             "id": 2,
#             "option": "100x100"
#         },
#         {
#             "id": 3,
#             "option": "Rosso - Rosso"
#         }
#     ],
#     attributes_en=[
#         {
#             "id": 2,
#             "option": "100x100-en"
#         },
#         {
#             "id": 3,
#             "option": "red-red-en"
#         }
#     ],
# )

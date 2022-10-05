# https://woocommerce.github.io/woocommerce-rest-api-docs/?python#product-properties

from auth import wcapi
from sql import query_sync_db

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
    ) -> dict:
    data = {
        "name": title_it,
        "type": _type,
        "description": description_it,
        "short_description": short_description_it,
        "categories": categories,
        "images": images,
        "attributes": attributes,
        "meta_data": meta_it
    }
    italian_product = wcapi.post("products", data).json()
    print(italian_product)
    data_en = {
        "name": title_en,
        "description": description_en,
        "short_description": short_description_en,
        "meta_data": meta_en,
        "lang": "en",
        "translation_of": italian_product['id']
    }
    english_product = wcapi.post("products", data_en).json()
    print(english_product)
    return {
        "italian_id": italian_product['id'],
        "english_id": english_product['id'],
    }


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
    ) -> dict:
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
    english_variation = wcapi.post(f"products/{str(product_id+1)}/variations", data_en).json()
    print(english_variation)
    return {
        "italian_id": italian_variation['id'],
        "english_id": english_variation['id'],
    }

def get_translation_id(post_id: int) -> int:
    query = """
        SELECT

        FROM

        WHERE
    """
    query_sync_db()
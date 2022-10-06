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
    ) -> dict:
    data = {
        "name": title_it,
        "type": _type,
        "description": description_it,
        "short_description": short_description_it,
        "categories": categories,
        "images": create_images_array(images),
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

def create_images_array(images_urls: list) -> list:
    return_list = [
        {"src": image_url.strip()}
        for image_url in images_urls.split(",")
    ] if images_urls else None
    print(return_list)
    return return_list

def retrieve_product(product_id: int) -> dict:
    return wcapi.get(f"products/{str(product_id)}").json()

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
        configurator_it: int,
        configurator_page_it: int,
        configurator_en: int,
        configurator_page_en: int,

    ) -> dict:
    """Attributes must be created beforehand"""
    image = {"src": image} if image else None
    data = {
        "sku": sku,
        "regular_price": regular_price,
        "image": image,
        "dimensions": dimensions,
        "attributes": attributes_it,
    }
    italian_variation = wcapi.post(f"products/{str(product_id)}/variations", data).json()
    add_vpc_config(configurator_it, configurator_page_it, product_id, italian_variation['id'])
    print("italian_variation")
    print(italian_variation)
    data_en = {
        "lang": "en",
        "translation_of": italian_variation['id'],
        "attributes": attributes_en
    }
    english_variation = wcapi.post(f"products/{str(product_id+1)}/variations", data_en).json()
    print("english_variation")
    print(english_variation)
    add_vpc_config(configurator_en, configurator_page_en, product_id+1, english_variation['id']+1)
    return {
        "italian_id": italian_variation['id'],
        "english_id": english_variation['id']+1,
    }

def add_vpc_config(
        configurator_id: int,
        configurator_page_id: int,
        product_id: int,
        variation_id: int
    ):
    current_config_object = get_current_config_object(product_id)
    current_config_object[variation_id] = {
        'config-id': configurator_id,
        'config-edit-link': configurator_page_id
    }
    data = {
        "meta_data": [
            {
                "key": "vpc-config",
                "value": current_config_object
            }
        ]
    }
    update_product(product_id, data)

def get_current_config_object(product_id: int) -> dict:
    meta_data = retrieve_product(product_id)['meta_data']
    for md in meta_data:
        if md['key'] == "vpc-config":
            return dict_bytes_value(md['value'])
    return {}

def dict_bytes_value(dict_value: dict) -> dict:
    return_dict = {}
    for key, value in dict_value.items():
        return_dict[int(key)] = {
            'config-id': value['config-id'],
            'config-edit-link': value['config-edit-link'],
        }
    return return_dict
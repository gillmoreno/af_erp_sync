import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.auth import wcapi
import logging


def create_product(
    title_it: str,
    title_en: str,
    description_it: str,
    description_en: str,
    short_description_it: str,
    short_description_en: str,
    categories: list,  # list of dicts
    cover_image: str,
    gallery_images: str,
    attributes: list,
    meta_it: list = [],
    meta_en: list = [],
) -> dict:
    data = {
        "name": title_it,
        "type": "variable",
        "description": description_it,
        "short_description": short_description_it,
        "categories": categories,
        "images": create_images_array(cover_image, gallery_images),
        "attributes": attributes,
        "meta_data": meta_it,
    }
    italian_product = wcapi.post("products", data).json()
    logging.info(italian_product)
    data_en = {
        "name": title_en,
        "description": description_en,
        "short_description": short_description_en,
        "meta_data": meta_en,
        "lang": "en",
        "translation_of": italian_product["id"],
    }
    english_product = wcapi.post("products", data_en).json()
    logging.info(english_product)
    return {
        "italian_id": italian_product["id"],
        "english_id": english_product["id"],
    }


def create_images_array(cover_image: str, gallery_images: str) -> list:
    return_list = []
    if cover_image:
        return_list.append(
            {"src": f"https://dev.arturofacchini.it/ftp_product_images/{cover_image}"}
        )
    if gallery_images:
        for image in gallery_images.split(","):
            return_list.append({"src": f"https://dev.arturofacchini.it/ftp_product_images/{image}"})
    return return_list


def retrieve_product(product_id: int) -> dict:
    return wcapi.get(f"products/{str(product_id)}").json()


def simple_update_product(product_id: int, data: dict):
    logging.info(wcapi.put(f"products/{str(product_id)}", data).json())


def update_product(
    product_id: int,
    product_id_en: int,
    title_it: str,
    title_en: str,
    description_it: str,
    description_en: str,
    short_description_it: str,
    short_description_en: str,
    categories: list,  # list of dicts
    cover_image: str,
    gallery_images: str,
    # attributes: list,
    meta_it: list = [],
    meta_en: list = [],
) -> None:
    data = {
        "name": title_it,
        "description": description_it,
        "short_description": short_description_it,
        "categories": categories,
        "images": create_images_array(cover_image, gallery_images),
        # "attributes": attributes,
        "meta_data": meta_it,
    }
    logging.info(wcapi.put(f"products/{str(product_id)}", data).json())
    data_en = {
        "name": title_en,
        "description": description_en,
        "short_description": short_description_en,
        "meta_data": meta_en,
        "lang": "en",
        "translation_of": f"products/{str(product_id)}",
    }
    logging.info(wcapi.put(f"products/{str(product_id_en)}", data_en).json())


def delete_product(product_id: int) -> None:
    logging.info(wcapi.delete(f"products/{str(product_id)}", params={"force": True}).json())


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
    description_it: str,
    description_en: str,
) -> dict:
    """Attributes must be created beforehand"""
    image = {"src": f"https://dev.arturofacchini.it/ftp_product_images/{image}"} if image else None
    data = {
        "sku": sku,
        "regular_price": regular_price,
        "image": image,
        "dimensions": dimensions,
        "attributes": attributes_it,
        "description": description_it,
    }
    print("product_id")
    print(product_id)
    italian_variation = wcapi.post(f"products/{str(product_id)}/variations", data).json()
    print(italian_variation)
    add_vpc_config(configurator_it, configurator_page_it, product_id, italian_variation["id"])
    logging.info("italian_variation")
    logging.info(italian_variation)
    data_en = {
        "lang": "en",
        "translation_of": italian_variation["id"],
        "attributes": attributes_en,
        "description": description_en,
    }
    english_variation = wcapi.post(f"products/{str(product_id+1)}/variations", data_en).json()
    logging.info("english_variation")
    logging.info(english_variation)
    add_vpc_config(
        configurator_en, configurator_page_en, product_id + 1, english_variation["id"] + 1
    )
    return {
        "italian_id": italian_variation["id"],
        "english_id": english_variation["id"] + 1,
    }


def update_product_variation(
    product_id: int,
    product_id_en: int,
    variation_id: int,
    variation_id_en: int,
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
    description_it: str,
    description_en: str,
    is_active: bool,
) -> None:
    """Attributes must be created beforehand"""
    image = {"src": image} if image else None
    data = {
        "sku": sku,
        "regular_price": regular_price,
        "image": image,
        "dimensions": dimensions,
        "attributes": attributes_it,
        "description": description_it,
        "status": "publish" if is_active else "draft",
    }
    logging.info(
        wcapi.put(f"products/{str(product_id)}/variations/{str(variation_id)}", data).json()
    )
    add_vpc_config(configurator_it, configurator_page_it, product_id, variation_id)
    data_en = {
        "lang": "en",
        "translation_of": variation_id,
        "attributes": attributes_en,
        "description": description_en,
    }
    logging.info(
        wcapi.put(
            f"products/{str(product_id_en)}/variations/{str(variation_id_en)}", data_en
        ).json()
    )
    add_vpc_config(configurator_en, configurator_page_en, product_id_en, variation_id_en)


def add_vpc_config(
    configurator_id: int, configurator_page_id: int, product_id: int, variation_id: int
):
    current_config_object = get_current_config_object(product_id)
    current_config_object[variation_id] = {
        "config-id": configurator_id,
        "config-edit-link": configurator_page_id,
    }
    data = {"meta_data": [{"key": "vpc-config", "value": current_config_object}]}
    simple_update_product(product_id, data)


def get_current_config_object(product_id: int) -> dict:
    meta_data = retrieve_product(product_id)["meta_data"]
    for md in meta_data:
        if md["key"] == "vpc-config":
            return dict_bytes_value(md["value"])
    return {}


def dict_bytes_value(dict_value: dict) -> dict:
    return_dict = {}
    for key, value in dict_value.items():
        return_dict[int(key)] = {
            "config-id": value["config-id"],
            "config-edit-link": value["config-edit-link"],
        }
    return return_dict

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.auth import wcapi
from apis.sql import query_sync_db
import logging
import requests


def create_or_update_product(
    title_it: str,
    title_en: str,
    description_it: str,
    description_en: str,
    short_description_it: str,
    short_description_en: str,
    categories: list,  # list of dicts
    tags: list,
    cover_image: str,
    gallery_images: str,
    meta_it: list = [],
    meta_en: list = [],
    product_id: int = None,
    product_id_en: int = None,
):
    data = {
        "name": title_it,
        "type": "variable",
        "description": description_it,
        "short_description": short_description_it,
        "categories": categories,
        "tags": tags,
        "images": create_images_array(cover_image, gallery_images),
        "meta_data": meta_it,
    }
    if product_id:
        result = wcapi.put(f"products/{str(product_id)}", data).json()
    else:
        result = wcapi.post("products", data).json()
        product_id = result["id"]
    logging.info(f"product ID -> {str(product_id)}")
    data_en = {
        "name": title_en,
        "description": description_en,
        "short_description": short_description_en,
        "meta_data": meta_en,
        "lang": "en",
        "translation_of": product_id,
    }
    if product_id_en:
        result = wcapi.put(f"products/{str(product_id_en)}", data_en).json()
    else:
        result = wcapi.post("products", data_en).json()
        product_id_en = result["id"]
    logging.info(f"product ID -> {str(product_id_en)}")
    return {
        "italian_id": product_id,
        "english_id": product_id_en,
    }


def create_images_array(cover_image: str, gallery_images: str) -> list:
    return_list = []
    if cover_image:
        return_list.append(
            {"src": f"https://prod.arturofacchini.it/ftp_product_images/{cover_image}"}
        )
    if gallery_images:
        for image in gallery_images.split(","):
            return_list.append(
                {"src": f"https://prod.arturofacchini.it/ftp_product_images/{image}"}
            )
    return return_list


def retrieve_product(product_id: int) -> dict:
    return wcapi.get(f"products/{str(product_id)}").json()


def simple_update_product(product_id: int, data: dict):
    updated_product = wcapi.put(f"products/{str(product_id)}", data).json()
    logging.info(f"updated_product ID -> {str(updated_product['id'])}")


def delete_product(product_id: int) -> None:
    logging.info(wcapi.delete(f"products/{str(product_id)}", params={"force": True}).json())


def create_or_update_product_variation(
    product_id: int,
    product_id_en: int,
    sku: str,
    regular_price: str,
    sale_price: str,
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
    meta_data: dict = {},
    is_active: bool = True,
    variation_id: int = None,
    variation_id_en: int = None,
):
    """Attributes must be created beforehand"""
    image = {"src": f"https://prod.arturofacchini.it/ftp_product_images/{image}"} if image else None
    data = {
        "sku": sku,
        "regular_price": regular_price,
        "sale_price": sale_price,
        "image": image,
        "dimensions": dimensions,
        "attributes": attributes_it,
        "description": description_it,
        "status": "publish" if is_active else "draft",
        "meta_data": meta_data,
    }
    if variation_id:
        response = wcapi.put(
            f"products/{str(product_id)}/variations/{str(variation_id)}", data
        ).json()
    else:
        response = wcapi.post(f"products/{str(product_id)}/variations", data).json()
        variation_id = response["id"]
    logging.info(f"variation ID -> {str(variation_id)}")
    add_vpc_config(configurator_it, configurator_page_it, product_id, variation_id)
    data_en = {
        "lang": "en",
        "translation_of": variation_id,
        "attributes": attributes_en,
        "description": description_en,
        "meta_data": meta_data,
    }
    if variation_id_en:
        response = wcapi.put(
            f"products/{str(product_id_en)}/variations/{str(variation_id_en)}", data_en
        ).json()
    else:
        response = wcapi.post(f"products/{str(product_id_en)}/variations", data_en).json()
        variation_id_en = response["id"] + 1
        add_vpc_config(configurator_en, configurator_page_en, product_id_en, variation_id_en)
        wcapi.put(f"products/{str(product_id_en)}/variations/{str(variation_id_en)}", data_en)
    logging.info(f"variation_en ID -> {variation_id_en}")
    return {
        "italian_id": variation_id,
        "english_id": variation_id_en,
    }


def create_product_brand(product_id: int, brand_name: str, id_sam_erp: str):
    url = f"http://prod.arturofacchini.it//wp-json/wc/v3/create-brand?product_id={str(product_id)}&brand_name={brand_name}"
    product_brand = requests.request("GET", url)
    sync_product_brand(id_sam_erp, product_brand.json()[0]["term_id"])
    return product_brand


def relate_product_brand(product_id: int, brand_id: int):
    url = f"http://prod.arturofacchini.it//wp-json/wc/v3/relate-brand?product_id={str(product_id)}&brand_id={str(brand_id)}"
    requests.request("GET", url)


def create_product_tag_color(product_id: int, color_name_it: str, color_name_en: str):
    url = f"http://prod.arturofacchini.it//wp-json/wc/v3/create-color?product_id={str(product_id)}&color_name={str(color_name_it)}&color_name_en={str(color_name_en)}"
    return requests.request("GET", url)


def relate_product_tag_color(product_id: int, id_wp: int):
    url = f"http://prod.arturofacchini.it//wp-json/wc/v3/relate-color?product_id={str(product_id)}&color_id={str(id_wp)}"
    requests.request("GET", url)


def sync_product_brand(id_sam_erp: str, id_wp: int):
    query = f"""
        UPDATE 
            product_brands 
        SET 
            id_wp={str(id_wp)}
        WHERE 
            id_sam_erp='{id_sam_erp}';
    """
    query_sync_db(query, False, True)


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

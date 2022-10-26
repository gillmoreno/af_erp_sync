import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db
from slugify import slugify
from utils import print_name
from products.products_wp_apis import *
from products.products__common import *
from apis.db_queries import get_products_out_of_sync
import logging


@print_name
def update_products():
    products_to_update = get_products_out_of_sync(False, False)
    if not products_to_update:
        logging.info("--> NO PRODUCTS TO UPDATE\n...\n")
    for product in products_to_update:
        update_product(
            product_id=product["id_wp"],
            product_id_en=product["id_wp_en"],
            title_it=product["title_it"],
            title_en=product["title_en"],
            description_it=product["description_it"],
            description_en=product["description_en"],
            short_description_it=product["short_description_it"],
            short_description_en=product["short_description_en"],
            categories=[{"id": product["category"]}],
            cover_image=product["cover_image"],
            gallery_images=product["gallery"],
            # attributes=product['attributes'],
            meta_it=[{"key": "_yoast_wpseo_metadesc", "value": product["meta_description_it"]}],
            meta_en=[{"key": "_yoast_wpseo_metadesc", "value": product["meta_description_en"]}],
        )
        sync_updated_product(product["id_sam_erp"])


def sync_updated_product(id_sam_erp: str) -> None:
    query = f"""
        UPDATE 
            products
        SET 
            in_sync=1
        WHERE 
            id_sam_erp='{id_sam_erp}';
    """
    query_sync_db(query, False, True)


def update_variations():
    variations_to_update = get_products_out_of_sync(False, True)
    if not variations_to_update:
        logging.info("--> NO VARIATIONS TO UPDATE\n...\n")
    for variation in variations_to_update:
        product_attributes = get_product_attributes(variation["id_parent_sam_erp"])
        parent_product_attributes = [
            {
                "id": 2,
                "variation": True,
                "visible": True,
                "options": product_attributes["dimensions"],
            },
            {
                "id": 3,
                "variation": True,
                "visible": True,
                "options": product_attributes["colors_it"],
            },
        ]
        product_id = get_product_wp_id(variation["id_parent_sam_erp"])
        simple_update_product(product_id, {"attributes": parent_product_attributes})
        update_product_variation(
            product_id=get_wp_variation_id(variation["id_parent_sam_erp"])["id_wp"],
            product_id_en=get_wp_variation_id(variation["id_parent_sam_erp"])["id_wp_en"],
            variation_id=variation["id_wp"],
            variation_id_en=variation["id_wp_en"],
            is_active=variation["is_active"],
            sku=variation["sku"],
            regular_price=str(variation["regular_price"]),
            sale_price=str(variation["sale_price"]),
            image=variation["image_"],
            dimensions={
                "length": str(variation["length_"]),
                "width": str(variation["width"]),
                "height": str(variation["height"]),
            },
            attributes_it=[
                {"id": 2, "option": slugify(variation["dimensions"])},
                {"id": 3, "option": slugify(variation["color_it"])},
            ],
            attributes_en=[
                {"id": 2, "option": slugify(f"{variation['dimensions']}-en")},
                {"id": 3, "option": slugify(f"{variation['color_en']}-en")},
            ],
            configurator_it=variation["configurator_it"],
            configurator_page_it=variation["configurator_page_it"],
            configurator_en=variation["configurator_en"],
            configurator_page_en=variation["configurator_page_en"],
            description_it=variation["description_it"],
            description_en=variation["description_en"],
        )
        sync_updated_variation(variation["sku"])


def get_wp_variation_id(id_sam_erp: str) -> None:
    query = f"""
        SELECT
            id_wp, id_wp_en
        FROM
            products
        WHERE
            id_sam_erp='{id_sam_erp}'
    """
    return query_sync_db(query, True)[0]


def sync_updated_variation(sku: str) -> None:
    query = f"""
        UPDATE 
            variations
        SET 
            in_sync=1
        WHERE 
            sku='{sku}';
    """
    query_sync_db(query, False, True)


if "__main__" in __name__:
    update_products()
    update_variations()

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db
from slugify import slugify
from products.products_wp_apis import *
from products.products__common import *
from utils import print_name
from db_queries import get_products_out_of_sync
import logging


@print_name
def create_parent_products():
    products_to_create = get_products_out_of_sync(new_only=True, is_variation=False)
    if not products_to_create:
        logging.info("--> NO PRODUCTS TO CREATE\n...\n")
    for product in products_to_create:
        wp_product = create_or_update_product(
            title_it=product["title_it"],
            title_en=product["title_en"],
            description_it=product["description_it"],
            description_en=product["description_en"],
            short_description_it=product["short_description_it"],
            short_description_en=product["short_description_en"],
            categories=[{"id": product["category"]}],
            tags=tag_list(product["tags"]),
            cover_image=product["cover_image"],
            gallery_images=product["gallery"],
            meta_it=[{"key": "_yoast_wpseo_metadesc", "value": product["meta_description_it"]}],
            meta_en=[{"key": "_yoast_wpseo_metadesc", "value": product["meta_description_en"]}],
        )
        sync_new_product(product["id_sam_erp"], wp_product)


def sync_new_product(id_sam_erp: str, wp_product: dict):
    query = f"""
        UPDATE 
            products 
        SET 
            in_sync=1,
            id_wp={str(wp_product['italian_id'])},
            id_wp_en={str(wp_product['english_id'])}
        WHERE 
            id_sam_erp='{id_sam_erp}';
    """
    query_sync_db(query, False, True)


@print_name
def create_variations():
    variations_to_create = get_products_out_of_sync(new_only=True, is_variation=True)
    if not variations_to_create:
        logging.info("--> NO VARIATIONS TO CREATE\n...\n")
    for variation in variations_to_create:
        dimensions = get_dimensions(variation["variation_dimensions_id"])
        colors = get_colors(variation["variation_colors_id"])
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
        product_id, product_id_en = get_product_wp_id(variation["id_parent_sam_erp"])
        simple_update_product(product_id, {"attributes": parent_product_attributes})
        wp_variation = create_or_update_product_variation(
            product_id=product_id,
            product_id_en=product_id_en,
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
                {"id": 2, "option": slugify(dimensions)},
                {"id": 3, "option": slugify(colors["value_it"])},
            ],
            attributes_en=[
                {"id": 2, "option": slugify(f"{dimensions}-en")},
                {"id": 3, "option": slugify(f"{colors['value_it']}-en")},
            ],
            description_it=variation["description_it"],
            description_en=variation["description_en"],
            configurator_it=variation["configurator_it"],
            configurator_page_it=variation["configurator_page_it"],
            configurator_en=variation["configurator_en"],
            configurator_page_en=variation["configurator_page_en"],
        )
        sync_new_variation(variation["sku"], wp_variation)


def get_dimensions(id_sam_erp: str) -> str:
    query = f"""
        SELECT 
            value_
        FROM 
            variation_dimensions
        WHERE
            id_sam_erp='{id_sam_erp}'
    """
    return query_sync_db(query, True)[0]["value_"]


def get_colors(id_sam_erp: str) -> dict:
    query = f"""
        SELECT 
            value_it, value_en
        FROM 
            variation_colors
        WHERE
            id_sam_erp='{id_sam_erp}'
    """
    return query_sync_db(query, True)[0]


def sync_new_variation(sku: str, wp_variation: dict):
    query = f"""
        UPDATE 
            variations 
        SET 
            in_sync=1,
            id_wp={str(wp_variation['italian_id'])},
            id_wp_en={str(wp_variation['english_id'])}
        WHERE 
            sku='{sku}';
    """
    query_sync_db(query, False, True)

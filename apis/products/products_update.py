from loguru import logger
from apis.db_queries import get_products_out_of_sync
from products.products__common import *
from products.products_wp_apis import *
from utils import print_name
from slugify import slugify
from apis.sql import query_sync_db
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@print_name
def update_products():
    products_to_update = get_products_out_of_sync(False, False)
    if not products_to_update:
        logger.info("--> NO PRODUCTS TO UPDATE\n...\n")
    for product in products_to_update:
        create_or_update_product(
            product_id=product["id_wp"],
            product_id_en=product["id_wp_en"],
            title_it=product["title_it"],
            title_en=product["title_en"],
            description_it=product["description_it"],
            description_en=product["description_en"],
            short_description_it=product["short_description_it"],
            short_description_en=product["short_description_en"],
            categories=get_categories_list(product["category"]),
            tags=tag_list(product["tags"]),
            cover_image=product["cover_image"],
            gallery_images=product["gallery"],
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


@print_name
def update_variations():
    variations_to_update = get_products_out_of_sync(False, True)
    if not variations_to_update:
        logger.info("--> NO VARIATIONS TO UPDATE\n...\n")
    for variation in variations_to_update:
        dimensions = get_dimensions(variation["variation_dimensions_id"])
        variation_colors_id = variation["variation_colors_id"]
        if not variation_colors_id:
            variation_colors_id = "PREDEF"
        colors = get_colors(variation_colors_id)
        product_attributes = get_product_attributes(
            variation["id_parent_sam_erp"])
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
        try:
            simple_update_product(product_id, {"attributes": parent_product_attributes})
        except Exception as e:
            logger.error(f"simple_update_product() -> product_id = {str(product_id)}")
            logger.error(e)
            continue

        pricelist_dict = get_price_list(variation["sku"])
        meta_data = [
            {"key": "pbq_pricing_type_enable", "value": "enable"},
            {"key": "pbq_pricing_type", "value": "fixed"},
            {"key": "pbq_table_layout", "value": "hover_table"},
            {"key": "_alg_wc_pq_min", "value": variation["quantity_min"]},
            {"key": "_alg_wc_pq_step", "value": variation["quantity_min"]},
        ]
        meta_data.append(
            {
                "key": "pbq_discount_table_data",
                "value": pricelist_dict["quantity_discounted_prices"],
            }
        )
        create_or_update_product_variation(
            product_id=product_id,
            product_id_en=product_id_en,
            variation_id=variation["id_wp"],
            variation_id_en=variation["id_wp_en"],
            is_active=variation["is_active"],
            sku=variation["sku"],
            regular_price=pricelist_dict["regular_price"],
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
                {"id": 3, "option": slugify(f"{colors['value_en']}-en")},
            ],
            configurator_it=variation["configurator_it"],
            configurator_page_it=variation["configurator_page_it"],
            configurator_en=variation["configurator_en"],
            configurator_page_en=variation["configurator_page_en"],
            description_it=variation["description_it"],
            description_en=variation["description_en"],
            meta_data=meta_data,
        )
        associate_product_tag_color(colors, product_id)
        sync_updated_variation(variation["sku"])


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

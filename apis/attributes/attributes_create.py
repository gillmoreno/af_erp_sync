from loguru import logger
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db
import itertools
from slugify import slugify
from utils import print_name
from attributes.attributes_wp_apis import *
from typing import List


def get_out_of_sync_product_attributes() -> List[str]:
    query = """
        SELECT 
            id_sam_erp, value_
        FROM 
            variation_dimensions
        WHERE
            id_wp is NULL
    """
    variation_dimensions = query_sync_db(query, True)
    query = """
        SELECT 
            id_sam_erp, value_it, value_en
        FROM 
            variation_colors
        WHERE
            id_wp is NULL
    """
    variation_colors = query_sync_db(query, True)
    print(variation_colors)
    return (variation_dimensions, variation_colors)


def create_attributes_terms(dimensions_options: List[dict], colors_options: List[dict]):
    create_colors_attribute_terms(colors_options)
    create_dimensions_attribute_terms(dimensions_options)


def create_colors_attribute_terms(colors_options: List[dict]):
    for color in colors_options:
        try:
            # color_id = create_attribute_term(3, color["value_it"], color["value_en"])
            color_id = create_attribute_term(3, (color["value_it"]).title(), (color["value_en"]).title())
            sync_new_attribute("variation_colors", color["id_sam_erp"], color_id)
        except Exception as e:
            logger.error(e)


def create_dimensions_attribute_terms(dimensions_options: List[dict]):
    for dimensions in dimensions_options:
        dimensions_id = create_attribute_term(2, dimensions["value_"], dimensions["value_"])
        sync_new_attribute("variation_dimensions", dimensions["id_sam_erp"], dimensions_id)


def sync_new_attribute(table: str, id_sam_erp: str, id_wp: int):
    query = f"""
        UPDATE 
            {table}
        SET 
            id_wp={str(id_wp)}
        WHERE 
            id_sam_erp='{id_sam_erp}';
    """
    query_sync_db(query, False, True)


@print_name
def create_attributes():
    dimensions_options, colors_options = get_out_of_sync_product_attributes()
    create_attributes_terms(dimensions_options, colors_options)

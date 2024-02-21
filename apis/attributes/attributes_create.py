"""
Provides functionalities to create or update product attributes (like dimensions and colors) in WordPress,
based on data from an external ERP system.

This module fetches unsynced product attribute data (dimensions and colors) from the ERP system and
uses WordPress API calls to create or update these attributes in the WordPress system.

Functions:
    get_out_of_sync_product_attributes() -> List[str]:
        Fetches product attributes that are out of sync between the ERP system and WordPress.

    create_attributes_terms(dimensions_options: List[dict], colors_options: List[dict]):
        Creates or updates attribute terms in WordPress for dimensions and colors.

Dependencies:
    - loguru: For logging.
    - os, sys: For path manipulations and system operations.
    - itertools, slugify: For data manipulation and slug creation.
    - utils, attributes_wp_apis: For additional utilities and WordPress API interactions.
"""

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
    """
    Fetches lists of product attributes related to dimensions and colors that are not yet synced with WordPress.

    Retrieves dimension and color attributes from the local database where the WordPress ID (`id_wp`) is NULL,
    indicating that these attributes have not been synced to WordPress.

    Returns:
        A tuple containing two lists: one for unsynced dimension attributes and one for unsynced color attributes,
        each with relevant ERP ID and value information.
    """
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
    """
    Creates or updates terms for product attributes in WordPress based on provided dimension and color options.

    Args:
        colors_options (List[dict]): A list of dictionaries containing color options to be synced.

    Utilizes WordPress API calls to create or update attribute terms for both dimensions and colors in WordPress,
    ensuring that product attributes in WordPress reflect the current data from the ERP system.
    """
    for color in colors_options:
        try:
            # color_id = create_attribute_term(3, color["value_it"], color["value_en"])
            color_id = create_attribute_term(3, (color["value_it"]).title(), (color["value_en"]).title())
            sync_new_attribute("variation_colors", color["id_sam_erp"], color_id)
        except Exception as e:
            logger.error(e)


def create_dimensions_attribute_terms(dimensions_options: List[dict]):
    """
    Creates or updates WordPress attribute terms for product dimensions and colors.

    This function interfaces with WordPress to ensure that each dimension and color option from the ERP system
    is represented as an attribute term in WordPress. It involves creating new terms for attributes that do not
    yet exist in WordPress and updating existing ones if necessary.

    Args:
        dimensions_options (List[dict]): Dimension options to be synced, with each dictionary representing a
                                         dimension attribute (e.g., length, width, height).

    The function constructs requests to the WordPress REST API to create or update attribute terms, utilizing
    the `attributes_wp_apis` module for API interactions.
    """
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

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
            dimensions, color_it, color_en 
        FROM 
            variations
    """
    attributes = query_sync_db(query, True)
    dimensions_options = []
    colors_options = []
    for attribute in attributes:
        dimensions_options.append(attribute["dimensions"])
        colors_options.append((attribute["color_it"], attribute["color_en"]))
    return list(set(dimensions_options)), list(set(colors_options))


def create_attributes_terms(dimensions_options: List[str], colors_options: List[tuple]):
    colors_options_it = [color[0] for color in colors_options]
    colors_options_en = [color[1] for color in colors_options]
    create_dimensions_attribute_terms(dimensions_options)
    create_colors_attribute_terms(colors_options_it, colors_options_en)


def create_dimensions_attribute_terms(dimensions_options: List[str]):
    non_existing_dimensions = get_non_existing_attributes(dimensions_options, 2)
    for dimensions in non_existing_dimensions:
        create_attribute_term(2, dimensions["value"], dimensions["value"])


def create_colors_attribute_terms(colors_options_it: List[str], colors_options_en: List[str]):
    non_existing_colors = get_non_existing_attributes(colors_options_it, 3)
    for color in non_existing_colors:
        create_attribute_term(3, color["value"], colors_options_en[color["index"]])


def get_non_existing_attributes(options: List[str], attribute_id: int) -> List[dict]:
    return_list = []
    for i, option in enumerate(options):
        slug = slugify(option)
        if not search_attribute_by_slug(attribute_id, slug):
            return_list.append({"index": i, "value": option})
    return return_list


@print_name
def create_attributes():
    dimensions_options, colors_options = get_out_of_sync_product_attributes()
    create_attributes_terms(dimensions_options, colors_options)

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql import query_sync_db
import itertools
from slugify import slugify
from attributes.attributes_wp_apis import *


def get_out_of_sync_product_attributes() -> list:
    attributes = query_sync_db(
        "SELECT dimensions_options, colors_options_it, colors_options_en FROM products WHERE in_sync=0"
    )
    dimensions_options = []
    colors_options_it = []
    colors_options_en = []
    for attribute in attributes:
        dimensions_options.append(split_attributes(attribute[0]))
        colors_options_it.append(split_attributes(attribute[1]))
        colors_options_en.append(split_attributes(attribute[2]))
    return (
        list(itertools.chain(*dimensions_options)),
        list(itertools.chain(*colors_options_it)),
        list(itertools.chain(*colors_options_en)),
    )


def split_attributes(attributes: str) -> list:
    return [attribute.strip() for attribute in attributes.split(",")]


def create_attributes_terms(
    dimensions_options: list, colors_options_it: list, colors_options_en: list
):
    create_dimensions_attribute_terms(dimensions_options)
    create_colors_attribute_terms(colors_options_it, colors_options_en)


def create_dimensions_attribute_terms(dimensions_options: list):
    non_existing_dimensions = get_non_existing_attributes(dimensions_options, 2)
    for dimensions in non_existing_dimensions:
        create_attribute_term(2, dimensions["value"], dimensions["value"])


def create_colors_attribute_terms(colors_options_it: list, colors_options_en: list):
    non_existing_colors = get_non_existing_attributes(colors_options_it, 3)
    for color in non_existing_colors:
        create_attribute_term(3, color["value"], colors_options_en[color["index"]])


def get_non_existing_attributes(options: list, attribute_id: int) -> list:
    return_list = []
    for i, option in enumerate(options):
        slug = slugify(option)
        if not search_attribute_by_slug(attribute_id, slug):
            return_list.append({"index": i, "value": option})
    return return_list


def create_attributes():
    dimensions_options, colors_options_it, colors_options_en = get_out_of_sync_product_attributes()
    create_attributes_terms(dimensions_options, colors_options_it, colors_options_en)

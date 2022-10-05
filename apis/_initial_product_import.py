import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql import query_sync_db
import itertools
from slugify import slugify
from product import *
from attributes import *


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
    return list(itertools.chain(*dimensions_options)), \
           list(itertools.chain(*colors_options_it)), \
           list(itertools.chain(*colors_options_en))

def split_attributes(attributes: str) -> list:
    return [
        attribute.strip()
        for attribute in attributes.split(",")
    ]
    

def create_attributes_terms(
        dimensions_options: list,
        colors_options_it: list,
        colors_options_en: list
    ):
    create_dimensions_attribute_terms(dimensions_options)
    create_colors_attribute_terms(colors_options_it, colors_options_en)

def create_dimensions_attribute_terms(dimensions_options: list):
    non_existing_dimensions = get_non_existing_attributes(dimensions_options, 2)
    for dimensions in non_existing_dimensions:
        create_attribute_term(2, dimensions['value'], dimensions['value'])

def create_colors_attribute_terms(colors_options_it: list, colors_options_en: list):
    non_existing_colors = get_non_existing_attributes(colors_options_it, 3)
    for color in non_existing_colors:
        create_attribute_term(3, color['value'], colors_options_en[color['index']])

def get_non_existing_attributes(options: list, attribute_id: int) -> list:
    return_list = []
    for i, option in enumerate(options):
        slug = slugify(option)
        if not search_attribute_by_slug(attribute_id, slug):
            return_list.append({
                'index': i,
                'value': option
            })
    return return_list

def create_attributes():
    dimensions_options, colors_options_it, colors_options_en = get_out_of_sync_product_attributes()
    create_attributes_terms(dimensions_options, colors_options_it, colors_options_en)

def create_parent_products():
    products_to_create = get_products_out_of_sync(new_only=True, is_variation=False)
    for product in products_to_create:
        wp_product = create_product(
            title_it=product['title_it'],
            title_en=product['title_en'],
            _type="variable",
            description_it=product['description_it'],
            description_en=product['description_en'],
            short_description_it=product['short_description_it'],
            short_description_en=product['short_description_en'],
            categories=[{'id': product['category']}],
            attributes=[
                {
                    "id": 2,
                    "variation": True,
                    "visible": True,
                    "options": split_attributes(product['dimensions_options'])
                },
                {
                    "id": 3,
                    "variation": True,
                    "visible": True,
                    "options": split_attributes(product['colors_options_it'])
                },
            ],
            images="",
            meta_it = [
                {
                    "key": "_yoast_wpseo_metadesc",
                    "value": product['meta_description_it']
                }
            ],
            meta_en = [
                {
                    "key": "_yoast_wpseo_metadesc",
                    "value": product['meta_description_en']
                }
            ]
        )
        sync_new_product(product['id_sam_erp'], wp_product)

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

def update_parent_products():
    pass

def create_variations():
    variations_to_create = get_products_out_of_sync(new_only=True, is_variation=True)
    for variation in variations_to_create:
        product_id = get_product_wp_id(variation['id_parent_sam_erp'])
        wp_variation = create_product_variation(
            product_id=product_id,
            sku=variation['sku'],
            regular_price=str(variation['price']),
            image=variation['image_'],
            dimensions={
                'length': str(variation['length_']),
                'width': str(variation['width']),
                'height': str(variation['height'])
            },
            attributes_it=[
                {
                    "id": 2,
                    "option": slugify(variation['dimensions'])
                },
                {
                    "id": 3,
                    "option": slugify(variation['color_it'])
                }
            ],
            attributes_en=[
                {
                    "id": 2,
                    "option": slugify(f"{variation['dimensions']}-en")
                },
                {
                    "id": 3,
                    "option": slugify(f"{variation['color_en']}-en")
                }
            ],
        )
        sync_new_variation(variation['sku'], wp_variation)

def get_product_wp_id(id_parent_sam_erp: str) -> int:
    query = f"""
        SELECT
            id_wp
        FROM
            products
        WHERE
            id_sam_erp='{id_parent_sam_erp}'
    """
    return query_sync_db(query=query)[0][0]

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

def get_products_out_of_sync(new_only: bool, is_variation: bool) -> list:
    table = "variations" if is_variation else "products"
    query_for_new = "AND id_wp=0" if new_only else ""
    query = f"""
        SELECT 
            * 
        FROM 
            {table}
        WHERE
            in_sync=0 {query_for_new}
    """
    return_data = query_sync_db(query=query, dictionary=True)
    if not return_data:
        print("Non ci sono prodotti da sincrinizzare")
    return return_data




# create_attributes()
# create_parent_products()
# create_variations()
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql import query_sync_db
from slugify import slugify
from product import update_product
from _db_queries import get_products_out_of_sync


def update_products():
    products_to_update = get_products_out_of_sync(False, False)
    for product in products_to_update:
        update_product(
            product_id=product['id_wp'],
            product_id_en=product['id_wp_en'],
            title_it=product['title_it'],
            title_en=product['title_en'],
            description_it=product['description_it'],
            description_en=product['description_en'],
            short_description_it=product['short_description_it'],
            short_description_en=product['short_description_en'],
            categories=[{'id': product['category']}],
            images=product['gallery'],
            # attributes=product['attributes'],
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
        sync_updated_product(product['id_sam_erp'])

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


if "__main__" in __name__:
    update_products()
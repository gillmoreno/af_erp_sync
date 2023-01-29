import os, sys
import time
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sync_scripts import *
from apis.attributes.attributes_create import create_attributes
from apis.products.products_create import create_parent_products, create_variations
from apis.products.products_update import update_products, update_variations
from sam_tables_sync.product_brands import update_product_brands
from sam_tables_sync.products import update_products as sam_update_products
from sam_tables_sync.variation_colors import update_variation_colors
from sam_tables_sync.variation_dimensions import update_variation_dimensions
from sam_tables_sync.variation_pricelists import update_variation_pricelists
from sam_tables_sync.variations import update_variations as sam_update_variations


if "__main__" in __name__:
    start_time = time.time()
    # Update DB frontiera from SAM tables
    update_product_brands()
    update_variation_colors()
    update_variation_dimensions()
    update_variation_pricelists()
    sam_update_products()
    sam_update_variations()
    # Update Woocommerce from DB frontiera
    create_attributes()
    create_parent_products()
    create_variations()
    update_products()
    update_variations()
    logging.info(f"Sync prodotti, tempo -> {str(time.time() - start_time)}")

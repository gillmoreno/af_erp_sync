import os, sys
import time
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sync_scripts import *
from apis.attributes.attributes_create import create_attributes
from apis.products.products_create import create_parent_products, create_variations
from apis.products.products_update import update_products, update_variations

if "__main__" in __name__:
    start_time = time.time()
    create_attributes()
    create_parent_products()
    create_variations()
    update_products()
    update_variations()
    logging.info(f"Sync prodotti, tempo -> {str(time.time() - start_time)}")

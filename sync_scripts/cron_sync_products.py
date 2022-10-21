import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sync_scripts import *
from apis.products.products_update import update_products, update_variations

if "__main__" in __name__:
    update_products()
    update_variations()

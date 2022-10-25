import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sync_scripts import *
from apis.attributes.attributes_create import *
from apis.products.products_create import *


if "__main__" in __name__:
    import time

    start_time = time.time()
    create_attributes()
    create_parent_products()
    create_variations()
    print("TEMPO...")
    print(time.time() - start_time)

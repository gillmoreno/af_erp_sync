import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.orders.orders_create import create_new_orders_db_frontiera

if "__main__" in __name__:
    create_new_orders_db_frontiera()

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sync_scripts import *
from apis.customers.customers_update import update_customers_db_frontiera
from apis.customers.customers_create import create_new_customers_db_frontiera
from apis.customers.custumers_sync_status import sync_wp_user_status

if "__main__" in __name__:
    create_new_customers_db_frontiera()
    update_customers_db_frontiera()
    sync_wp_user_status()

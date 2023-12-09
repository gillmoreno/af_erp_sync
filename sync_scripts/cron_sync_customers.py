import os, sys
import time
from loguru import logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sync_scripts import *
from apis.customers.customers_update import update_customers_db_frontiera
from apis.customers.customers_create import create_new_customers_db_frontiera
from apis.customers.custumers_sync_status import sync_wp_user_status

if "__main__" in __name__:
    logger.info("Started sync customers...")
    start_time = time.time()
    sync_wp_user_status()
    create_new_customers_db_frontiera()
    update_customers_db_frontiera()
    logger.info(f"Sync customers, tempo -> {str(time.time() - start_time)}")

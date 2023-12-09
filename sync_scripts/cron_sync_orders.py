import os, sys
from loguru import logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.orders.orders_create import create_new_orders_db_frontiera

if "__main__" in __name__:
    logger.info("Executing create_new_orders_db_frontiera... sync orders")
    create_new_orders_db_frontiera()

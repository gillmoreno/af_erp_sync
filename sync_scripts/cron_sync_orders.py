"""
Synchronizes new order data from an external source into the local database.

This script is focused on integrating new orders into the local database system by invoking the
`create_new_orders_db_frontiera` function. It is part of a larger synchronization routine, ensuring
that order information is kept current and consistent across systems.

Functions:
    create_new_orders_db_frontiera: Responsible for creating new order records in the local database,
    reflecting orders placed through an external system (e.g., a WordPress site).

Usage:
    Intended to be run as part of a scheduled task (e.g., a cron job) to regularly update the local
    database with new orders from the external system. Proper configuration of environment variables
    and database connections is assumed.

Note:
    The script leverages the `loguru` library for logging purposes, providing visibility into the
    execution process and any potential issues encountered during the synchronization.
"""

import os, sys
from loguru import logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.orders.orders_create import create_new_orders_db_frontiera

if "__main__" in __name__:
    logger.info("Executing create_new_orders_db_frontiera... sync orders")
    create_new_orders_db_frontiera()

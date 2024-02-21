"""
Synchronizes customer information between a WordPress site and the local database.

This script coordinates the synchronization of customer data by performing several key operations:
- Syncing WordPress user statuses to reflect the latest user interactions or status changes.
- Creating new customers in the local database based on data from the WordPress site.
- Updating existing customer records in the local database to match the latest data from the WordPress site.

The script logs the initiation and completion of the sync process, providing a timestamped record of how long the synchronization takes.

Functions:
    sync_wp_user_status: Checks and updates the status of WordPress users to ensure local database alignment.
    create_new_customers_db_frontiera: Creates new customer records in the local database based on WordPress data.
    update_customers_db_frontiera: Updates existing customer records in the local database to reflect current WordPress data.

Usage:
    The script is intended to be run as a standalone scheduled task (e.g., via cron) to regularly sync customer data.
    Ensure that all necessary environment variables and database connections are correctly configured before running.

Note:
    This script relies on specific functions from the `apis.customers` module and assumes access to a configured WordPress site and local database.
"""

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

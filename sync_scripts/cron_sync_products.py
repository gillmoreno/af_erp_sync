"""
Orchestrates the synchronization of product information from external sources into the local database.

This script executes a series of operations to ensure that the local database reflects the latest
product data. This includes syncing stock levels, creating and updating product attributes, parent
products, variations, and applying updates from SAM tables to the local database for brands, colors,
dimensions, pricelists, and variations.

Functions:
    sync_stock: Synchronizes stock levels with the local database.
    create_attributes: Creates product attributes in the database.
    create_parent_products: Creates parent product entries.
    create_variations: Creates product variation entries.
    update_products: Updates existing product records.
    update_variations: Updates existing product variation records.
    update_product_brands, update_variation_colors, update_variation_dimensions,
    update_variation_pricelists, sam_update_products, sam_update_variations:
        Update various aspects of product data based on information from SAM tables.

Usage:
    Designed to be executed as part of a scheduled synchronization routine (e.g., via cron job), this
    script ensures the local database is kept in sync with external product data sources and internal
    updates from SAM tables.

Note:
    The script uses the `loguru` library for logging and measures execution time to monitor performance.
    It assumes proper configuration of environment variables and database connections.
"""

import os, sys
import time
from loguru import logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sync_scripts.cron_sync_stock import sync_stock
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
    sync_stock()
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
    logger.info(f"Sync prodotti, tempo -> {str(time.time() - start_time)}")

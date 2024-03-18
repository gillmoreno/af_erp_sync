import os, sys
import time
from loguru import logger
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db


def sync_stock():
    """
    Synchronizes stock levels for product variations from an external source into the local database.

    This function executes a SQL query that updates the stock levels of product variations in the local
    database. It matches stock information from the 'SAM_GIACENZE' table (an external system) with the SKUs
    of product variations stored in the local 'variations' table. The update is based on the presence of
    matching SKUs between these two sources.

    The function logs the start and successful completion of the stock synchronization process. It also
    prints database connection details, sourced from environment variables, for debugging purposes.

    Environment Variables:
        DB_USER, DB_PASSWORD, DB_HOST, DB_PORT: Used for database connection. Their values are printed
        out for debugging but are not directly used in the function.

    Side Effects:
        - Executes a SQL update query on the local database.
        - Logs the initiation and completion of the stock synchronization.

    Returns:
        None. The function aims to update the database and logs its actions but does not return a value.
    """

    logger.info("Synching stock...")
    query = """
        SELECT variations.sku AS sku, variations.stock AS old_stock, SAM_GIACENZE.szSemaforoID AS new_stock
        FROM variations
        JOIN SAM_GIACENZE ON SAM_GIACENZE.szArticoloID LIKE CONCAT('%', variations.sku, ' ', '%')
        WHERE variations.stock != SAM_GIACENZE.szSemaforoID
    """
    results_dict = query_sync_db(query, True)
    for result in results_dict:
        update_query = f"""
            UPDATE variations
            SET stock = {result["new_stock"]}, in_sync = 0
            WHERE sku = '{result["sku"]}'
        """
        query_sync_db(update_query, False, True)
    logger.info("Stock synched successfully!")


if "__main__" in __name__:
    sync_stock()

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
    query = f"""
        UPDATE variations
        SET stock = (
            SELECT szSemaforoID
            FROM SAM_GIACENZE
            WHERE SAM_GIACENZE.szArticoloID LIKE CONCAT('%', variations.sku, ' ', '%')
        )
        WHERE EXISTS (
            SELECT 1
            FROM SAM_GIACENZE
            WHERE SAM_GIACENZE.szArticoloID LIKE CONCAT('%', variations.sku, ' ', '%')
        );
    """
    query_sync_db(query, False, True)
    logger.info("Stock synched successfully!")


if "__main__" in __name__:
    sync_stock()

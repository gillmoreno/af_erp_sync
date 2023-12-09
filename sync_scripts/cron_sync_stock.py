import os, sys
import time
from loguru import logger
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db

def sync_stock():
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
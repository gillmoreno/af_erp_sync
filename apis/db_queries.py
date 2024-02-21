from apis.sql import query_sync_db
from loguru import logger


def get_products_out_of_sync(new_only: bool, is_variation: bool) -> list:
    """
    Retrieves a list of products or variations that are out of sync with an external system.

    This function queries the local database to find all products or variations that are marked
    as not in sync (in_sync=0). It can be configured to return only new items (those without a
    WordPress ID) and to differentiate between products and variations.

    Args:
        new_only (bool): If True, only items without a WordPress ID (id_wp is NULL) are returned.
        is_variation (bool): Determines whether to fetch variations (True) or products (False).

    Returns:
        list: A list of dictionaries, each representing a product or variation that is out of sync.
              Returns an empty list if there are no items to synchronize.

    The function logs a message if no items are found that meet the criteria for synchronization.
    """
    table = "variations" if is_variation else "products"
    query_for_new = "AND id_wp IS NULL" if new_only else ""
    query = f"""
        SELECT 
            * 
        FROM 
            {table}
        WHERE
            in_sync=0 {query_for_new}
    """
    return_data = query_sync_db(query=query, dictionary=True)
    if not return_data:
        logger.info("-> Non ci sono prodotti da sincronizzare")
    return return_data

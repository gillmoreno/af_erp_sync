import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db

print(os.path.basename(__file__))


def update_product_brands():
    """
    Updates the local database's `product_brands` table with brand information from the external `SAM_GENITORI` table.

    This function executes an SQL query that inserts new brand records into the `product_brands` table or updates
    existing records if there's a match on the ERP code (`id_sam_erp`). The brand's description (`value_`) and
    a corresponding WordPress ID (`id_wp`, if available) are used in the insertion or update process.

    The SQL operation uses an `ON DUPLICATE KEY UPDATE` clause to ensure that existing records are updated with
    new information from the `SAM_GENITORI` table without creating duplicate entries.

    Side Effects:
        - Executes an SQL insert/update operation on the `product_brands` table in the local database.
        - Logs the name of the executed script to the console for debugging purposes.

    Returns:
        None. The primary goal is to update the database without returning any value from the function.
    """
    query = """
        INSERT INTO product_brands (id_sam_erp, value_, id_wp)
        SELECT s.AC2Codice, s.AC2Descr, p.id_wp
        FROM SAM_GENITORI AS s
        LEFT JOIN product_brands AS p ON s.AC2Codice = p.id_sam_erp
        ON DUPLICATE KEY UPDATE value_ = s.AC2Descr;
    """
    query_sync_db(query, True, True)


if "__main__" in __name__:
    update_product_brands()

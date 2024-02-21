import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db

print(os.path.basename(__file__))


def update_products():
    """
    Updates the local database's `products` table with product information from the external `SAM_GENITORI` table.

    This function executes an SQL query to insert new product records into the `products` table or update
    existing records based on the ERP code (`id_sam_erp`). The insertion or update includes the product's
    ERP code, WordPress IDs (`id_wp`, `id_wp_en`), sync status (`in_sync`), titles in Italian (`title_it`)
    and English (`title_en`), category (`category`), and brand ID (`product_brand_id`).

    The function employs an `ON DUPLICATE KEY UPDATE` clause to ensure existing records are refreshed with
    the latest information from the `SAM_GENITORI` table without creating duplicate entries. Product titles
    and categories are dynamically constructed from the ERP data.

    Side Effects:
        - Executes an SQL insert/update operation on the `products` table in the local database.
        - Logs the name of the executed script to the console for operational tracking.

    Returns:
        None. The function's main objective is to update the database, and it does not return any value.
    """
    query = """
        INSERT INTO products (
            id_sam_erp, 
            id_wp,
            id_wp_en,
            in_sync,
            title_it,
            title_en,
            category,
            product_brand_id
        )
        SELECT 
            s.szCodice, 
            COALESCE(p.id_wp, NULL),
            COALESCE(p.id_wp_en, NULL),
            COALESCE(p.in_sync, 0),
            CONCAT(s.AC2Descr, ' ', s.AC4Descr),
            CONCAT(s.AC2Descr, ' ', s.AC4Descr),
            s.AC4Codice,
            s.AC2Codice
        FROM SAM_GENITORI AS s
        LEFT JOIN products AS p ON s.szCodice = p.id_sam_erp
        ON DUPLICATE KEY UPDATE
            title_it = CONCAT(s.AC2Descr, ' ', s.AC4Descr),
            title_en = CONCAT(s.AC2Descr, ' ', s.AC4Descr),
            category = s.AC4Codice,
            product_brand_id = s.AC2Codice,
            cover_image = s.ImgPrincipale,
            gallery = s.ImgGalleria,
            description_it = s.szDescrizione,
            description_en = s.szDescrizione;
    """
    query_sync_db(query, True, True)


if "__main__" in __name__:
    update_products()


# A query that helped me put values from products to SAM_GENITORI that will make it easier to put image names there
useful_query = """
    UPDATE SAM_GENITORI
    INNER JOIN products ON SAM_GENITORI.szDescrizione = products.description_it
    SET
    SAM_GENITORI.ImgPrincipale = products.cover_image,
    SAM_GENITORI.ImgGalleria = products.gallery
    
"""

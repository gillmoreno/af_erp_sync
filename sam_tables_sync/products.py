import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db

def update_products():
    query = """
        INSERT INTO products (
            id_sam_erp, 
            id_wp,
            id_wp_en,
            in_sync,
            title_it,
            title_en,
            category,
            product_brand_id,
            cover_image,
            gallery,
            description_it,
            description_en
        )
        SELECT 
            s.szCodice, 
            COALESCE(p.id_wp, NULL),
            COALESCE(p.id_wp_en, NULL),
            COALESCE(p.in_sync, 0),
            CONCAT(s.AC2Descr, ' ', s.AC4Descr),
            CONCAT(s.AC2Descr, ' ', s.AC4Descr),
            s.AC4Codice,
            s.AC2Codice,
            s.ImgPrincipale,
            s.ImgGalleria,
            s.szDescrizione,
            s.szDescrizione
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
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
            # tags,
            # meta_descriptiom_it,
            # meta_descriptiom_en,
            cover_image,
            gallery,
            description_it,
            description_en
            # short_description_it,
            # short_description_en
        )
        SELECT 
            s.szCodice, 
            p.id_wp,
            p.id_wp_en,
            COALESCE(p.in_sync, 0),
            CONCAT(s.AC2Descr, ' ', s.AC4Descr),
            CONCAT(s.AC2Descr, ' ', s.AC4Descr),
            REPLACE(s.AC4Codice, 'W', ''),
            AC2Codice,
            # tags,
            # meta_descriptiom_it,
            # meta_descriptiom_en,
            s.ImgPrincipale,
            s.ImgGalleria,
            szDescrizione,
            szDescrizione
            # short_description_it,
            # short_description_en
        FROM SAM_GENITORI AS s
        LEFT JOIN products AS p ON s.szCodice = p.id_sam_erp;
    """
    query_sync_db(query, True, True)

if "__main__" in __name__:
    update_products()
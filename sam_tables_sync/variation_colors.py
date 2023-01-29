import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db

def update_variation_colors():
    query = """
        INSERT INTO variation_colors (id_sam_erp, id_wp, value_it, value_en)
        SELECT s.szCodice, v.id_wp, s.szDescrizione, s.szDescrizione
        FROM SAM_ARTCLA AS s
        LEFT JOIN variation_colors AS v ON s.szCodice = v.id_sam_erp
        WHERE s.szTipoID = 2
        ON DUPLICATE KEY UPDATE value_it = s.szDescrizione, value_en = s.szDescrizione;
    """
    query_sync_db(query, True, True)

if "__main__" in __name__:
    update_variation_colors()
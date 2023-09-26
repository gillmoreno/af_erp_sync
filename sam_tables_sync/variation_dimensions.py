import os, sys
from typing import List, Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db

print(os.path.basename(__file__))

def update_variation_dimensions():
    concat = """ CONCAT(
        ROUND(v.szLunghezza, 0),
        'x',
        ROUND(v.szLarghezza, 0),
        IF(ROUND(v.szAltezza, 0) > 0, 'x', ''),
        IF(ROUND(v.szAltezza, 0) > 0, ROUND(v.szAltezza, 0), '')
    )
    """
    query = f"""
        INSERT INTO variation_dimensions (id_sam_erp, id_wp)
        SELECT {concat}, COALESCE(d.id_wp, NULL)
        FROM SAM_VARIATIONS AS v
        LEFT JOIN variation_dimensions AS d ON d.id_sam_erp = {concat}
        ON DUPLICATE KEY UPDATE id_sam_erp = {concat}, id_wp = d.id_wp;
    """
    query_sync_db(query, True, True)
    query = """
        UPDATE variation_dimensions
        SET value_ = id_sam_erp;
    """
    query_sync_db(query, True, True)


if "__main__" in __name__:
    update_variation_dimensions()
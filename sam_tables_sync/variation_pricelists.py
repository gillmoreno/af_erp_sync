import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db

def update_variation_pricelists():
    query = """
        INSERT INTO variation_pricelists (sku, quantity, unit_price)
        SELECT 
            TRIM(p.szArticoloID),
            CASE WHEN p.dQuantita = 0 THEN 1 ELSE p.dQuantita END,
            p.dPrezzo
        FROM SAM_PRICELIST p
        JOIN SAM_VARIATIONS v ON TRIM(p.szArticoloID) = TRIM(v.szArticoloID)
        ON DUPLICATE KEY UPDATE unit_price=p.dPrezzo;
    """
    query_sync_db(query, False, True)

if "__main__" in __name__:
    update_variation_pricelists()
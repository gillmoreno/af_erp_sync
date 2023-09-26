import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db

print(os.path.basename(__file__))

def update_product_brands():
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
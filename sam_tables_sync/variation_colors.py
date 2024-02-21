import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db

print(os.path.basename(__file__))


def update_variation_colors():
    """
    Updates the `variation_colors` table with color information from the `SAM_ARTCLA` table of an external system.

    The function is designed to insert new color records into the `variation_colors` table or update existing records
    based on the ERP code (`id_sam_erp`). It includes handling for `NULL` ERP codes and ensures that color descriptions
    are unique and informative by potentially appending the ERP code to the description.

    Note:
        The script contains commented-out SQL queries that illustrate different approaches to managing color information,
        including handling `NULL` values for `id_sam_erp` and constructing color descriptions.

    Side Effects:
        - Executes an SQL insert/update operation on the `variation_colors` table in the local database.
        - Logs the name of the executed script to the console for operational tracking.

    Returns:
        None. The function's primary goal is to update the database, and it does not return any value.
    """
    # query = """
    #     INSERT INTO variation_colors (id_sam_erp, id_wp, value_it, value_en)
    #     SELECT s.szCodice, v.id_wp, s.szDescrizione, s.szDescrizione
    #     FROM SAM_ARTCLA AS s
    #     LEFT JOIN variation_colors AS v ON s.szCodice = v.id_sam_erp
    #     WHERE s.szTipoID = 2
    #     ON DUPLICATE KEY UPDATE value_it = s.szDescrizione, value_en = s.szDescrizione;
    # """

    # non gestisce id_sam_erp NULL
    # query = """
    #     INSERT INTO variation_colors (id_sam_erp, id_wp, value_it, value_en)
    #     SELECT s.szCodice, v.id_wp, CONCAT(s.szDescrizione,'_',s.szCodice), CONCAT(s.szDescrizione,'_',s.szCodice)
    #     FROM SAM_ARTCLA AS s
    #     LEFT JOIN variation_colors AS v ON s.szCodice = v.id_sam_erp
    #     WHERE s.szTipoID = 2
    #     ON DUPLICATE KEY UPDATE value_it = CONCAT(s.szDescrizione,'_',s.szCodice), value_en = CONCAT(s.szDescrizione,'_',s.szCodice);
    # """

    query = """
        INSERT INTO variation_colors (id_sam_erp, id_wp, value_it, value_en)
        SELECT 
            s.szCodice,
            v.id_wp, 
            CONCAT(s.szDescrizione,'_',s.szCodice),
            CONCAT(s.szDescrizione,'_',s.szCodice)
        FROM SAM_ARTCLA AS s
        LEFT JOIN variation_colors AS v ON s.szCodice = v.id_sam_erp
        WHERE s.szTipoID = 2
        ON DUPLICATE KEY UPDATE 
            value_it = CONCAT(s.szDescrizione,'_',s.szCodice),
            value_en = CONCAT(s.szDescrizione,'_',s.szCodice);
    """

    query_sync_db(query, True, True)

    query2 = """
        INSERT INTO variation_colors (id_sam_erp, value_it, value_en)
        SELECT 
            'PREDEF',
            'COLORE STANDARD',
            'STANDARD COLOR'
        FROM DUAL
        WHERE NOT EXISTS (SELECT 1 FROM variation_colors WHERE id_sam_erp = 'PREDEF');
    """

    query_sync_db(query2, True, True)


if "__main__" in __name__:
    update_variation_colors()

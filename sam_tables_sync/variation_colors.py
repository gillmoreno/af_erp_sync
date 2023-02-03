from apis.sql import query_sync_db
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def update_variation_colors():
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
        SELECT s.szCodice, v.id_wp, CONCAT(s.szDescrizione,'_',s.szCodice), CONCAT(s.szDescrizione,'_',s.szCodice)
        FROM SAM_ARTCLA AS s
        LEFT JOIN variation_colors AS v ON s.szCodice = v.id_sam_erp
        WHERE s.szTipoID = 2
        ON DUPLICATE KEY UPDATE value_it = CONCAT(s.szDescrizione,'_',s.szCodice), value_en = CONCAT(s.szDescrizione,'_',s.szCodice);
    """

    query_sync_db(query, True, True)

    query2 = """
        INSERT INTO variation_colors (id_sam_erp, value_it, value_en)
        SELECT 'PREDEF', 'COLORE STANDARD', 'STANDARD COLOR'
        FROM DUAL
        WHERE NOT EXISTS (SELECT 1 FROM variation_colors WHERE id_sam_erp = 'PREDEF');
    """

    query_sync_db(query2, True, True)


if "__main__" in __name__:
    update_variation_colors()

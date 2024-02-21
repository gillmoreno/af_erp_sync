import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db

print(os.path.basename(__file__))


def update_variations():
    """
    Updates the `variations` table with detailed product variation information from an external system.

    This function executes an SQL query to insert new records into the `variations` table or update
    existing ones with comprehensive data fields. These fields include WordPress IDs, synchronization
    status, parent ERP IDs, activity status, SKU, descriptions in Italian and English, minimum quantity,
    image URLs, physical dimensions (length, width, height), color and dimension IDs, and configurator
    details for both Italian and English versions.

    The function aims to ensure that the local database's variation records are current and accurately
    reflect the data from the external system, supporting synchronized e-commerce operations.

    Side Effects:
        - Executes an SQL insert/update operation on the `variations` table in the local database.
        - Logs the name of the executed script to the console for operational tracking.

    Returns:
        None. The function's primary purpose is to update the database without returning any value.
    """
    query = """
        INSERT INTO variations (
            id_wp,
            id_wp_en,
            in_sync,
            id_parent_sam_erp,
            is_active,
            sku,
            description_it,
            description_en,
            quantity_min,
            image_,
            length_,
            width,
            height,
            variation_colors_id,
            variation_dimensions_id,
            configurator_it,
            configurator_en,
            configurator_page_it,
            configurator_page_en
        )
        SELECT 
            v.id_wp,
            v.id_wp_en,
            COALESCE(v.in_sync, 0),
            CONCAT(s.szGEN2, ' | W', s.WEB_CATEGORIA),
            COALESCE(v.is_active, 1),
            TRIM(s.szArticoloID),
            s.szDescrizione,
            s.szDescrizione,
            s.dQuantitaMinima,
            TRIM(s.szImmagine),
            s.szLunghezza,
            s.szLarghezza,
            s.szAltezza,
            COALESCE(vc.id_sam_erp, "PREDEF"),
            CONCAT(
                ROUND(s.szLunghezza, 0),
                'x',
                ROUND(s.szLarghezza, 0),
                IF(ROUND(s.szAltezza, 0) > 0, 'x', ''),
                IF(ROUND(s.szAltezza, 0) > 0, ROUND(s.szAltezza, 0), '')
            ),
            s.WEBcfgITA,
            s.WEBcfgENG,
            78,
            293
        FROM SAM_VARIATIONS AS s
        LEFT JOIN variations AS v 
            ON TRIM(s.szArticoloID) = v.sku
        LEFT JOIN variation_colors as vc 
            ON vc.id_sam_erp = s.szGEN3
        ON DUPLICATE KEY UPDATE
            id_parent_sam_erp = CONCAT(s.szGEN2, ' | W', s.WEB_CATEGORIA),
            is_active = COALESCE(v.is_active, 1),
            description_it = s.szDescrizione,
            description_en = s.szDescrizione,
            quantity_min = s.dQuantitaMinima,
            image_ = TRIM(s.szImmagine),
            length_ = s.szLunghezza,
            width = s.szLarghezza,
            height = s.szAltezza,
            variation_colors_id = COALESCE(vc.id_sam_erp, "PREDEF"),
            variation_dimensions_id = CONCAT(
                ROUND(s.szLunghezza, 0),
                'x',
                ROUND(s.szLarghezza, 0),
                IF(ROUND(s.szAltezza, 0) > 0, 'x', ''),
                IF(ROUND(s.szAltezza, 0) > 0, ROUND(s.szAltezza, 0), '')
            ),
            configurator_it = s.WEBcfgITA,
            configurator_en = s.WEBcfgENG,
            configurator_page_it = 78,
            configurator_page_en = 293;
    """
    query_sync_db(query, True, True)


if "__main__" in __name__:
    update_variations()

import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db

print(os.path.basename(__file__))

def update_variations():
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

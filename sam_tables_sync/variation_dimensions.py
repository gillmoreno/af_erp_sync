import os, sys
from typing import List, Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db

print(os.path.basename(__file__))


def update_variation_dimensions():
    """
    Updates the `variation_dimensions` table with dimension information from the `SAM_VARIATIONS` table.

    This function constructs a concatenated string representation of product variation dimensions (length x width x height)
    and uses this representation to insert new records into the `variation_dimensions` table or update existing ones. The
    process involves two main SQL operations: one to insert or update the dimension records based on the concatenated
    dimension string, and another to ensure that the `value_` field of the table is correctly set to this string.

    The dimension string is constructed with consideration for variations that may not have a specified height, omitting
    the height dimension when it is not greater than zero.

    Side Effects:
        - Executes SQL insert/update operations on the `variation_dimensions` table in the local database.
        - Constructs and updates dimension strings for product variations, ensuring accuracy and consistency of dimension data.

    Returns:
        None. The primary aim is to update the database, and the function does not return a value.
    """
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

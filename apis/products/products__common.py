import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db


def get_product_attributes(id_parent_sam_erp: str) -> dict:
    query = f"""
        SELECT 
            dimensions, color_it 
        FROM 
            variations 
        WHERE 
            id_parent_sam_erp='{id_parent_sam_erp}';
    """
    result = query_sync_db(query, True)
    return_dict = {"dimensions": [], "colors_it": []}
    for option in result:
        return_dict["dimensions"].append(option["dimensions"])
        return_dict["colors_it"].append(option["color_it"])
    return return_dict


def get_product_wp_id(id_parent_sam_erp: str) -> int:
    query = f"""
        SELECT
            id_wp, id_wp_en
        FROM
            products
        WHERE
            id_sam_erp='{id_parent_sam_erp}'
    """
    result = query_sync_db(query=query)[0]
    return result[0], result[1]


def tag_list(tags: str) -> list:
    if tags:
        tags = tags.replace(" ", "")
        tags = tags.split(",")
        return [{"id": tag} for tag in tags]
    else:
        return []

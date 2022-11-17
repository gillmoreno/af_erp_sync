import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db


def get_product_attributes(id_parent_sam_erp: str) -> dict:
    query = f"""
        SELECT 
            vc.value_it, vd.value_
        FROM 
            variations as v
        INNER JOIN 
            variation_colors as vc
        ON 
            vc.id_sam_erp = v.variation_colors_id
        INNER JOIN 
            variation_dimensions as vd
        ON 
            vd.id_sam_erp = v.variation_dimensions_id
        WHERE 
            v.id_parent_sam_erp = '{id_parent_sam_erp}';
    """
    result = query_sync_db(query, True)
    return_dict = {"dimensions": [], "colors_it": []}
    for option in result:
        return_dict["dimensions"].append(option["value_"])
        return_dict["colors_it"].append(option["value_it"])
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


def get_dimensions(id_sam_erp: str) -> str:
    query = f"""
        SELECT 
            value_
        FROM 
            variation_dimensions
        WHERE
            id_sam_erp='{id_sam_erp}'
    """
    return query_sync_db(query, True)[0]["value_"]


def get_colors(id_sam_erp: str) -> dict:
    query = f"""
        SELECT 
            value_it, value_en
        FROM 
            variation_colors
        WHERE
            id_sam_erp='{id_sam_erp}'
    """
    return query_sync_db(query, True)[0]


def get_product_brand(id_sam_erp: str) -> int:
    query = f"""
        SELECT 
            id_wp, value_
        FROM 
            product_brands
        WHERE
            id_sam_erp='{id_sam_erp}'
    """
    return query_sync_db(query, True)[0]

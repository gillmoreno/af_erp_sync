from .products_wp_apis import *
from apis.sql import query_sync_db
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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


def get_price_list(sku: str) -> dict:
    query = f"""
        SELECT 
            quantity, unit_price
        FROM
            variation_pricelists
        WHERE
            sku='{sku}';
    """
    pricelist = query_sync_db(query, True)
    regular_price = 0
    quantity_discounted_prices = []
    for price in pricelist:
        if price["quantity"] == 1:
            regular_price = price["unit_price"]
            break
    for price in pricelist:
        if price["quantity"] != 1:
            quantity_discounted_prices.append(
                {
                    "pbq_quantity": price["quantity"],
                    "pbq_discount": str(round((regular_price - price["unit_price"]), 2)),
                }
            )
    return {
        "regular_price": str(regular_price),
        "quantity_discounted_prices": quantity_discounted_prices,
    }


def associate_product_tag_color(colors: dict, product_id: int):
    colors_italian, colors_english = get_individual_colors(colors)
    for i, color in enumerate(colors_italian):
        product_tag_color = get_product_tag_color(color)
        if product_tag_color:
            id_wp = product_tag_color[0]["id_wp"]
            relate_product_tag_color(product_id, id_wp)
        else:
            response = create_product_tag_color(product_id, color, colors_english[i])
            create_product_tag_color_db_frontiera(
                response.json()[0]["term_id"], color, colors_english[i]
            )


def get_individual_colors(colors: dict) -> tuple:
    # colors_italian = colors["value_it"].replace(" ", "").split("-")
    # colors_english = colors["value_en"].replace(" ", "").split("-")
    colors_italian = colors["value_it"].replace(" ", "").split("_")[0].split("-")
    
    colors_english = colors["value_en"].replace(" ", "").split("_")[0].split("-")
    
    return colors_italian, colors_english


def get_product_tag_color(color: str) -> int:
    query = f"""
        SELECT 
            id_wp 
        FROM
            product_tag_colors
        WHERE
            value_it='{color}';
    """
    return query_sync_db(query, True)


def create_product_tag_color_db_frontiera(id_wp: int, color_it: str, color_en: str):
    query = f"""
        INSERT INTO 
            product_tag_colors(
                id_wp,
                value_it,
                value_en
            ) 
        VALUES 
            (
                {id_wp},
                '{color_it}',
                '{color_en}'
            ); 
    """
    query_sync_db(query, False, True)

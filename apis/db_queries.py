from apis.sql import query_sync_db


def get_products_out_of_sync(new_only: bool, is_variation: bool) -> list:
    table = "variations" if is_variation else "products"
    query_for_new = "AND id_wp=0" if new_only else ""
    query = f"""
        SELECT 
            * 
        FROM 
            {table}
        WHERE
            in_sync=0 {query_for_new}
    """
    return_data = query_sync_db(query=query, dictionary=True)
    if not return_data:
        print("Non ci sono prodotti da sincronizzare")
    return return_data

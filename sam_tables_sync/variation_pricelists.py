import os, sys
from loguru import logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apis.sql import query_sync_db

print(os.path.basename(__file__))

def log_func(func):
    def wrapper(*args, **kwargs):
        logger.info(f"Executing: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_func
def get_unique_skus():
    query = """
        SELECT sku FROM variations;
    """
    result = query_sync_db(query)
    return [item[0] for item in result]

@log_func
def get_skus_occurrances_in_variation_pricelists(skus: list) -> dict:
    string_in = str(skus).replace("[","").replace("]","")
    query = f"""
        SELECT sku, COUNT(*) as occurrences
        FROM variation_pricelists
        WHERE sku IN ({string_in})
        GROUP BY sku;
    """
    return query_sync_db(query, True)

@log_func
def get_skus_occurrances_in_sam_pricelist(skus: list) -> dict:
    where_clause = ' OR '.join([f"szArticoloID LIKE '%{sku} %'" for sku in skus])
    query = f"""
        SELECT szArticoloID, COUNT(*) as occurrences
        FROM SAM_PRICELIST
        WHERE {where_clause}
        GROUP BY szArticoloID;
    """
    return query_sync_db(query, True)

@log_func
def find_mismatched_occurrences(list1, list2):
    # Convert list2 into a dictionary for easy lookup
    dict2 = {item['szArticoloID']: item['occurrences'] for item in list2}

    # List for mismatched skus
    mismatched_skus = []

    # Check each sku in list1
    for item in list1:
        sku = item['sku']
        occurrences = item['occurrences']

        # Check if the sku exists in list2 and has different occurrences
        if sku in dict2 and dict2[sku] != occurrences:
            mismatched_skus.append(sku)

    return mismatched_skus

@log_func
def delete_mismatched_skus(skus):
    string_in = str(skus).replace("[","").replace("]","")
    query = f"""l
        DELETE FROM variation_pricelists
        WHERE sku IN ({string_in});
    """
    query_sync_db(query, False, True)
    
@log_func
def add_variation_pricelists():
    query = """
        INSERT INTO variation_pricelists (sku, quantity, unit_price)
        SELECT 
            TRIM(p.szArticoloID),
            CASE WHEN p.dQuantita = 0 THEN 1 ELSE p.dQuantita END,
            p.dPrezzo
        FROM SAM_PRICELIST p
        JOIN SAM_VARIATIONS v ON TRIM(p.szArticoloID) = TRIM(v.szArticoloID)
        ON DUPLICATE KEY UPDATE unit_price=p.dPrezzo;
    """
    query_sync_db(query, False, True)

@log_func
def get_out_of_sync_skus():
    query = """
        SELECT DISTINCT sku
        FROM variation_pricelists
        WHERE in_sync = 0;
    """
    result = query_sync_db(query)
    return [item[0] for item in result]

@log_func
def put_variations_out_of_sync(skus):
    string_in = str(skus).replace("[","").replace("]","")
    query = f"""
        UPDATE variations
        SET in_sync = 0
        WHERE sku IN ({string_in});
    """
    query_sync_db(query, False, True)

@log_func
def put_variation_pricelists_back_in_sync():
    query = f"""
        UPDATE variation_pricelists
        SET in_sync = 1;
    """
    query_sync_db(query, False, True)

@log_func
def update_variation_pricelists():
    logger.info("Updating pricelists...")
    unique_skus = get_unique_skus()
    occurrances_wp = get_skus_occurrances_in_variation_pricelists(unique_skus)
    occurrances_sam = get_skus_occurrances_in_sam_pricelist(unique_skus)
    for item in occurrances_sam:
        item['szArticoloID'] = item['szArticoloID'].strip()
    
    mismatched_skus = find_mismatched_occurrences(occurrances_wp, occurrances_sam)
    delete_mismatched_skus(mismatched_skus)
    add_variation_pricelists()
    out_of_sync_skus = get_out_of_sync_skus()
    put_variations_out_of_sync(out_of_sync_skus)
    put_variation_pricelists_back_in_sync()


if "__main__" in __name__:
    update_variation_pricelists()
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql import query_sync_db


def get_db_frontiera_users_wp_ids():
    query = """
        SELECT
            id_wp
        FROM
            customers
    """
    return query_sync_db(query)

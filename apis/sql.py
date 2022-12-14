import os
from dotenv import load_dotenv
import mysql.connector
import logging

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def query_sync_db(query, dictionary=False, write=False, multi=False):
    try:
        config = {
            "user": DB_USER,
            "password": DB_PASSWORD,
            "host": DB_HOST,
            "port": DB_PORT,
            "database": DB_NAME,
            "raise_on_warnings": True,
        }

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=dictionary)
        cursor.execute(query, multi=multi)
        return_value = [x for x in cursor]
        if write:
            cnx.commit()
            return_value = cursor.lastrowid
        cursor.close()
        cnx.close()
        return return_value
    except Exception as e:
        logging.info(e)

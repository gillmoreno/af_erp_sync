import os
from dotenv import load_dotenv
import mysql.connector
from loguru import logger

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def query_sync_db(query, dictionary=False, write=False, multi=False):
    """
    Executes a SQL query against the database with optional configurations for result formatting and query type.

    Connects to the MySQL database using configurations specified in environment variables, executes the provided
    SQL query, and optionally commits the transaction for write operations. It can return the results in a dictionary
    format and supports executing multiple statements.

    Args:
        query (str): The SQL query to be executed.
        dictionary (bool, optional): If True, the query results are returned as a list of dictionaries.
                                     Defaults to False, returning a list of tuples.
        write (bool, optional): If True, executes the query as a write operation, committing the transaction.
                                Defaults to False.
        multi (bool, optional): If True, allows the execution of multiple queries separated by semicolons.
                                Defaults to False.

    Returns:
        Depending on the arguments, this function can return:
        - A list of dictionaries (or tuples) containing the query results, for read operations.
        - The last row ID inserted, for write operations.
        - An empty list if the query does not return any results.

    Raises:
        Exception: Logs and prints any exception that occurs during the database operation.

    Utilizes the mysql.connector package for database connections and operations, with error handling
    to log any issues encountered during execution.
    """
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
        print(e)
        logger.info(e)

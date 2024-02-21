from typing import List
from loguru import logger


def get_meta_data_key(meta_data: List[dict], key) -> str:
    """
    Searches for a specific key within a list of dictionaries representing meta data and returns its value.

    Args:
        meta_data (List[dict]): A list of dictionaries, each containing 'key' and 'value' pairs of meta data.
        key (str): The meta data key to search for.

    Returns:
        str: The value associated with the specified key if found, or "NOT FOUND" if the key does not exist in any dictionary within the list.

    This function iterates through each dictionary in the list, checking for the presence of the specified key and returning its associated value when found.
    """
    for data in meta_data:
        if data["key"] == key:
            return data["value"]
    return "NOT FOUND"


def print_name(func):
    """
    A decorator that logs the start and finish of the execution of the function it decorates.

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: A wrapper function that logs the execution start and finish messages, then calls the original function.

    Usage:
        Can be applied to any function to automatically log when its execution starts and finishes, enhancing
        logging for debugging and monitoring purposes.

    Example:
        @print_name
        def some_function():
            pass
    """

    def wrapper():
        logger.info(f"--> START executing {func.__name__}")
        func()
        logger.info(f"--> FINISHED executing {func.__name__}\n ...")

    return wrapper

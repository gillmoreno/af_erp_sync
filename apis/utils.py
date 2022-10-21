from typing import List


def get_meta_data_key(meta_data: List[dict], key) -> str:
    for data in meta_data:
        if data["key"] == key:
            return data["value"]
    return "NOT FOUND"


def print_name(func):
    def wrapper():
        print(f"--> START executing {func.__name__}")
        func()
        print(f"--> FINISHED executing {func.__name__}\n ...")

    return wrapper

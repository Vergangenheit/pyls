from typing import Any

def is_string_list(data: Any) -> bool:
    if isinstance(data, list):
        if isinstance(data[0], str):
            return True
    return False

def is_tuple_list(data: Any) -> bool:
    if isinstance(data, list):
        if isinstance(data[0], tuple):
            return True
    return False

def is_probable_file(name: str) -> bool:
    return ('.' in name and not name.endswith('.')) or name.isupper()
from typing import List, Tuple
from argparse import Namespace
from utils.utils import is_string_list, is_tuple_list
import time

def formatter_function(data: List) -> None:
    if is_string_list(data):
        print(" ".join(data))
    elif is_tuple_list(data):
        for content in data:
            print(" ".join(format_tuple(content)))

def format_tuple(content: Tuple) -> List:
    data = []
    # first permission as is
    if isinstance(content[0], str) is False:
        raise ValueError("permissions should be a string")
    data.append(content[0])
    if isinstance(content[1], (int, float)):
        # its a unix timestamp to convert into YY DD HH:MM like "Nov 14 14:57"
        data.append(time.strftime("%b %d %H:%M", time.gmtime(content[1])))
    elif isinstance(content[1], str):
        # its already a formatted time
        data.append(content[1])
    if isinstance(content[2], str) is False:
        raise ValueError("name should be a string")
    data.append(content[2])

    return data
from typing import List, Tuple
from argparse import Namespace
from utils.utils import is_string_list, is_tuple_list
import time

"""
Function responsible for formatting and printing the output
"""
def formatter_function(data: List) -> None:
    if is_string_list(data):
        print(" ".join(data))
    elif is_tuple_list(data):
        max_size_width = max(len(str(entry[1])) for entry in data)
        for content in data:
            formatted = format_tuple(content)
            print(f"{formatted[0]} {formatted[1]:>{max_size_width}} {formatted[2]} {formatted[3]}")

"""
Formats the tuple data before printing
"""
def format_tuple(content: Tuple) -> List:
    data = []
    # first permission as is
    if isinstance(content[0], str) is False:
        raise ValueError("permissions should be a string")
    data.append(content[0])
    if not isinstance(content[1], (int, float)):
        raise ValueError("size should be a number")
    data.append(str(content[1]))
    if isinstance(content[2], (int, float)):
        # its a unix timestamp to convert into YY DD HH:MM like "Nov 14 14:57"
        data.append(time.strftime("%b %d %H:%M", time.gmtime(content[2])))
    elif isinstance(content[2], str):
        # its already a formatted time
        data.append(content[2])
    if isinstance(content[3], str) is False:
        raise ValueError("name should be a string")
    data.append(content[3])

    return data
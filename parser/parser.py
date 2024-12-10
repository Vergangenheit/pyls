from typing import List, Tuple, Dict, Union
import json
from argparse import Namespace
import os
from utils.utils import is_string_list, is_tuple_list


"""
This function aggregates all the logic
"""
def parser_function(filepath: str, options: List[str]) -> List:
    data = extract_from_file(filepath)
    # collect all the options
    options_map = {"l": option_l, "A": option_a, "ls": option_ls, "r": option_r}
    for option in options:
        if option in options_map:
            data = options_map[option](data)

    return data

def option_r(data: List) -> List:
    return data[::-1]

def option_l(data: Dict) -> List[Tuple]:
    contents = []
    for content in data["contents"]:
        contents.append((content["permissions"], content["time_modified"], content["name"]))

    return contents


def option_ls(data: Union[Dict, List[str], List[Tuple]]) -> List:
    if is_string_list(data):
        contents = []
        for content in data:
            if content.startswith("."):
                continue
            contents.append(content)

        return contents
    elif isinstance(data, dict):
        contents = []
        for content in data["contents"]:
            if content["name"].startswith("."):
                continue
            contents.append(content["name"])

        return contents
    elif is_tuple_list(data):
        contents = []
        for content in data:
            if content[2].startswith("."):
                continue
            contents.append(content)

        return contents
    else:
        raise ValueError("data type not supported")

    

def option_a(data: Union[Dict, List[Tuple]]) -> List:
    if isinstance(data, dict):
        contents = []
        for content in data["contents"]:
            if isinstance(content["name"], str):
                contents.append(content["name"])

        return contents
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("data type not supported")


def extract_from_file(filepath: str) -> Dict:
    if filepath == "":
        raise ValueError("file path is required")
    if os.path.exists(filepath) is False:
        raise ValueError("file does not exist")
    # open the file and if it is not a json file, raise an error
    with open(filepath) as json_file:
        try:
            data = json.load(json_file)
        except json.JSONDecodeError:
            raise ValueError("file is not a json file")
    # check if the deserialized data is not empty
    if not data:
        raise ValueError("json data is empty")
    
    return data
            

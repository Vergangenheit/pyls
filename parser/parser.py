from typing import List, Dict, Union
import json
from argparse import Namespace
import os

def parser_function(filepath: str, options: List[str]) -> List:
    data = extract_from_file(filepath)
    # collect all the options
    options_map = {"A": option_a, "ls": option_ls}

    # output the data in "contents" key to the console following linux ls protocol
    for option in options:
        if option in options_map:
            data = options_map[option](data)

    return data

def option_ls(data: Union[Dict, List]) -> List:
    if isinstance(data, list):
        contents = []
        for content in data:
            if content.startswith("."):
                continue
            contents.append(content)

        return contents
    elif isinstance(data, Dict):
        contents = []
        for content in data["contents"]:
            if content["name"].startswith("."):
                continue
            contents.append(content["name"])

        return contents
    

def option_a(data: Dict) -> List:
    contents = []
    for content in data["contents"]:
        if isinstance(content["name"], str):
            contents.append(content["name"])

    return contents


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
            

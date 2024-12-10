from typing import List
import json
from argparse import Namespace
import os

def parser_function(args: Namespace) -> List:
    if args is None:
        raise ValueError("args is required")
    if args.file == "":
        raise ValueError("file path is required")
    if os.path.exists(args.file) is False:
        raise ValueError("file does not exist")
    # open the file and if it is not a json file, raise an error
    with open(args.file) as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError("file is not a json file")
    # check if the deserialized data is not empty
    if not data:
        raise ValueError("json data is empty")
    # output the data in "contents" key to the console following linux ls protocol
    contents = []
    for content in data["contents"]:
        if isinstance(content["name"], str):
            if content["name"].startswith("."):
                continue
            contents.append(content["name"])

    return contents
            

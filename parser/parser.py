from typing import List, Tuple, Dict, Union
import json
from argparse import Namespace
import os
from utils.utils import is_string_list, is_tuple_list, is_probable_file


"""
This function aggregates all the logic
"""
def parser_function(filepath: str, options: List[str]) -> Union[List[str], List[Tuple]]:
    data = extract_from_file(filepath)
    # collect all the options
    options_map = {"l": option_l, "t": option_t, "A": option_a, "ls": option_ls, "r": option_r, 
                   "dir": option_filter_dir, "file": option_filter_file}
    # Check if a string with the prefix 'navigate:' exists and extract it
    navigate_string = next((s for s in options if s.startswith("navigate:")), None)
    if navigate_string:
        data = navigate_path(navigate_string.split(":")[1], data)
    for option in options:
        if option in options_map:
            data = options_map[option](data)

    return data

def navigate_path(path: str, data: Dict) -> Union[Dict, List[Tuple]]:
    if path == ".":
        return data
    # Split the input path into components
    path_components = path.split('/')

    # Initialize a list to store the resources
    resources = []

    def traverse(directory: Dict, components: List[str]) -> None:
        # If no more components are left, return the contents of the current directory
        if not components:
            for item in directory['contents']:
                # Append the tuple (name, permissions, size, time_modified)
                resources.append((
                    item['permissions'], item['size'], item['time_modified'], item['name']
                ))
            return

        # Look for the next directory or file in the current directory's contents
        next_component = components[0]
        for item in directory['contents']:
            if item['name'] == next_component:
                # If it's a directory and there's more to the path, recurse
                if 'contents' in item:
                    traverse(item, components[1:])
                else:
                    # If it's a file, add its information and stop
                    resources.append((
                        item['permissions'], item['size'], item['time_modified'], item['name']
                    ))
                return

        # If we didn't find the item, raise a ValueError
        raise ValueError(f"cannot access {'/'.join(components)}: No such file or directory")

    # Start the traversal from the root directory (filesystem_json)
    try:
        traverse(data, path_components)
    except ValueError as e:
        # Raise ValueError if the path is not found
        raise ValueError(f"cannot access {path}: No such file or directory") from e

    return resources
      

"""
Filters the data to include only directories 
"""
def option_filter_dir(data: Union[List[Tuple], List[str]]) -> Union[List[Tuple], List[str]]:
    if is_string_list(data):
        filtered_data = []
        for content in data:
            if is_probable_file(content):
                continue
            filtered_data.append(content)
        return filtered_data
    
    if is_tuple_list(data):
        filtered_data = []
        for content in data:
            if is_probable_file(content[3]):
                continue
            filtered_data.append(content)
        return filtered_data

"""
Filters the data to include only files
"""  
def option_filter_file(data: Union[List[Tuple], List[str]]) -> Union[List[Tuple], List[str]]:
    if is_string_list(data):
        filtered_data = []
        for content in data:
            if is_probable_file(content):
                filtered_data.append(content)
        return filtered_data
    
    if is_tuple_list(data):
        filtered_data = []
        for content in data:
            if is_probable_file(content[3]):
                filtered_data.append(content)
        return filtered_data

"""
Sorts the data by time modified
"""
def option_t(data: List[Tuple]) -> List[Tuple]:
    return sorted(data, key=lambda x: x[2])

"""
Reverses the data
"""
def option_r(data: List) -> List:
    return data[::-1]

"""
Formats the data to include permissions, size, time modified and name
"""
def option_l(data: Union[Dict, List]) -> List[Tuple]:
    if isinstance(data, dict):
        contents = []
        for content in data["contents"]:
            contents.append((content["permissions"], content["size"], content["time_modified"], content["name"]))

        return contents
    else:
        # data is already extracted in the required format
        return data

"""
Extracts the contents names from the data excluding hidden files
"""
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
            if content[3].startswith("."):
                continue
            contents.append(content)

        return contents
    else:
        raise ValueError("data type not supported")

    
"""
Extracts the contents names from the data
"""
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

"""
Extracts the data from the json file
"""
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
            

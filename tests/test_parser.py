from argparse import Namespace
from pytest import raises
from parser.parser import parser_function
import os
import json


def test_nofile():
    with raises(ValueError, match="file path is required"):
        parser_function("", [])

def test_file_not_exist():
    with raises(ValueError, match="file does not exist"):
        parser_function("nonexistent.json", [])

def test_file_not_json():
    with raises(ValueError, match="file is not a json file"):
        parser_function("tests/test_parser.py", [])

def test_empty_json():
    empty_dict = {}
    with open("tests/empty.json", "w") as file:
        json.dump(empty_dict, file, indent=4)
    with raises(ValueError, match="json data is empty"):
        parser_function("tests/empty.json", [])
    os.remove("tests/empty.json")

def test_ls():
    test_data = {"contents": [{"name": ".hidden"}, {"name": "visible"}]}
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["ls"])

    assert data == ["visible"]

    os.remove("tests/hidden.json")

def test_A():
    test_data = {"contents": [{"name": ".hidden"}, {"name": "visible"}]}
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["A"])

    assert data == [".hidden", "visible"]

    os.remove("tests/hidden.json")

def test_l_A():
    test_data = {
        "contents": [
            {"name": ".hidden", "time_modified": 0, "permissions": "perm1"}, 
            {"name": "visible", "time_modified": 1, "permissions": "perm2"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["l", "A"])

    assert data == [("perm1", 0, ".hidden"), ("perm2", 1, "visible")]

    os.remove("tests/hidden.json")

def test_l_ls():
    test_data = {
        "contents": [
            {"name": ".hidden", "time_modified": 0, "permissions": "perm1"}, 
            {"name": "visible", "time_modified": 1, "permissions": "perm2"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["l", "ls"])

    assert data == [("perm2", 1, "visible")]

    os.remove("tests/hidden.json")
    
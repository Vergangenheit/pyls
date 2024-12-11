from argparse import Namespace
from pytest import raises
from parser.parser import parser_function, option_r
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

def test_l_r():
    test_data = {
        "contents": [
            {"name": ".hidden", "time_modified": 0, "permissions": "perm1"}, 
            {"name": "visible", "time_modified": 1, "permissions": "perm2"},
            {"name": "visible2", "time_modified": 2, "permissions": "perm3"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["l", "ls","r"])

    assert data == [("perm3", 2, "visible2"), ("perm2", 1, "visible")]

    os.remove("tests/hidden.json")

def test_l_A_r():
    test_data = {
        "contents": [
            {"name": ".hidden", "time_modified": 0, "permissions": "perm1"}, 
            {"name": "visible", "time_modified": 1, "permissions": "perm2"},
            {"name": "visible2", "time_modified": 2, "permissions": "perm3"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["l", "A","r"])

    assert data == [("perm3", 2, "visible2"), ("perm2", 1, "visible"), ("perm1", 0, ".hidden")]

    os.remove("tests/hidden.json")

def test_l_A_t():
    test_data = {
        "contents": [
            {"name": ".hidden", "time_modified": 1, "permissions": "perm1"}, 
            {"name": "visible", "time_modified": 0, "permissions": "perm2"},
            {"name": "visible2", "time_modified": 2, "permissions": "perm3"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["l", "A","t"])

    assert data == [("perm2", 0, "visible"), ("perm1", 1, ".hidden"), ("perm3", 2, "visible2")]

    os.remove("tests/hidden.json")  

def test_l_t_r():
    test_data = {
        "contents": [
            {"name": ".hidden", "time_modified": 1, "permissions": "perm1"}, 
            {"name": "visible", "time_modified": 0, "permissions": "perm2"},
            {"name": "visible2", "time_modified": 2, "permissions": "perm3"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["l", "t", "ls", "r"])

    assert data == [("perm3", 2, "visible2"), ("perm2", 0, "visible")]

    os.remove("tests/hidden.json")

def test_l_t_A_r():
    test_data = {
        "contents": [
            {"name": ".hidden", "time_modified": 1, "permissions": "perm1"}, 
            {"name": "visible", "time_modified": 0, "permissions": "perm2"},
            {"name": "visible2", "time_modified": 2, "permissions": "perm3"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["l", "t", "A", "r"])

    assert data == [("perm3", 2, "visible2"), ("perm1", 1, ".hidden"), ("perm2", 0, "visible")]

    os.remove("tests/hidden.json")

def test_r():
    test_data = {
        "contents": [
            {"name": ".hidden", "time_modified": 1, "permissions": "perm1"}, 
            {"name": "visible", "time_modified": 0, "permissions": "perm2"},
            {"name": "visible2", "time_modified": 2, "permissions": "perm3"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["ls","r"])

    assert data == ["visible2", "visible"]

    os.remove("tests/hidden.json")

def test_option_r():
    test_data = [
        ".hidden", 
        "visible",
        "visible2"
    ]
    data = option_r(test_data)

    assert data == ["visible2", "visible", ".hidden"]
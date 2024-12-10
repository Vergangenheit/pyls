from argparse import Namespace
from pytest import raises
from parser.parser import parser_function
import os
import json


def test_nofile():
    with raises(ValueError, match="file path is required"):
        parser_function(Namespace(file=""))

def test_noargs():
    with raises(ValueError, match="args is required"):
        parser_function(None)

def test_file_not_exist():
    with raises(ValueError, match="file does not exist"):
        parser_function(Namespace(file="nonexistent.json"))

def test_file_not_json():
    with raises(ValueError, match="file is not a json file"):
        parser_function(Namespace(file="tests/test_parser.py"))

def test_empty_json():
    empty_dict = {}
    with open("tests/empty.json", "w") as file:
        json.dump(empty_dict, file, indent=4)
    with raises(ValueError, match="json data is empty"):
        parser_function(Namespace(file="tests/empty.json"))
    os.remove("tests/empty.json")

def test_hidden_files():
    test_data = {"contents": [{"name": ".hidden"}, {"name": "visible"}]}
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function(Namespace(file="tests/hidden.json"))

    assert data == ["visible"]

    os.remove("tests/hidden.json")
    
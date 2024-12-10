from argparse import Namespace
from pytest import raises
from parser.parser import parser_function


def test_nofile():
    with raises(ValueError, match="file path is required"):
        parser_function(Namespace(file=""))

def test_noargs():
    with raises(ValueError, match="args is required"):
        parser_function(None)

def test_file_not_exist():
    with raises(ValueError, match="file does not exist"):
        parser_function(Namespace(file="nonexistent.json"))


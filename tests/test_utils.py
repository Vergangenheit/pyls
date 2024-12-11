from utils.utils import is_string_list, is_tuple_list, is_probable_file

def test_is_string_list():
    assert is_string_list(["string"]) == True

    assert is_string_list([1]) == False

def test_is_tuple_list():
    assert is_tuple_list([("tuple", 1)]) == True

    assert is_tuple_list(["string"]) == False

def test_is_probable_file():
    assert is_probable_file("file.txt") == True

    assert is_probable_file("file") == False

    assert is_probable_file(".file") == True

    assert is_probable_file("visible") == False

    assert is_probable_file("VISIBLE") == True
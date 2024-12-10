from utils.utils import is_string_list, is_tuple_list

def test_is_string_list():
    assert is_string_list(["string"]) == True

    assert is_string_list([1]) == False

def test_is_tuple_list():
    assert is_tuple_list([("tuple", 1)]) == True

    assert is_tuple_list(["string"]) == False
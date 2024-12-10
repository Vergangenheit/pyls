from pyls.formatter import format_tuple
from pytest import raises

def test_format_tuple():
    formatted_str = format_tuple(("permissions", 1699941437, "name"))

    assert formatted_str == ["permissions", "Nov 14 05:57", "name"]

def test_format_tuple_timeasstr():
    formatted_str = format_tuple(("permissions", "October 12 09:00:00", "name"))

    assert formatted_str == ["permissions", "October 12 09:00:00", "name"]

def test_format_tuple_invalid_permissions():
    with raises(ValueError, match="permissions should be a string"):
        format_tuple((1, 1699941437, "name"))

def test_format_tuple_invalid_name():
    with raises(ValueError, match="name should be a string"):
        format_tuple(("permissions", 1699941437, 1))

from pytest import raises
from pyls.parser import parser_function, option_r, navigate_path
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
            {"name": ".hidden", "size": 32, "time_modified": 0, 
             "permissions": "perm1"}, 
            {"name": "visible", "size": 33, "time_modified": 1, 
             "permissions": "perm2"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["l", "A"])

    assert data == [("perm1", 32, 0, ".hidden"), ("perm2", 33, 1, "visible")]

    os.remove("tests/hidden.json")


def test_l_ls():
    test_data = {
        "contents": [
            {"name": ".hidden", "size": 32, "time_modified": 0, 
             "permissions": "perm1"}, 
            {"name": "visible", "size": 33, "time_modified": 1, 
             "permissions": "perm2"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["l", "ls"])

    assert data == [("perm2", 33, 1, "visible")]

    os.remove("tests/hidden.json")


def test_l_r():
    test_data = {
        "contents": [
            {"name": ".hidden", "size": 32, "time_modified": 0, 
             "permissions": "perm1"}, 
            {"name": "visible", "size": 30, "time_modified": 1, 
             "permissions": "perm2"},
            {"name": "visible2", "size": 39, "time_modified": 2, 
             "permissions": "perm3"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", 
                           ["l", "ls", "r"])

    assert data == [("perm3", 39, 2, "visible2"), ("perm2", 30, 1, "visible")]

    os.remove("tests/hidden.json")


def test_l_A_r():
    test_data = {
        "contents": [
            {"name": ".hidden", "size": 32, "time_modified": 0, 
             "permissions": "perm1"}, 
            {"name": "visible", "size": 30,  "time_modified": 1, 
             "permissions": "perm2"},
            {"name": "visible2", "size": 39, "time_modified": 2, 
             "permissions": "perm3"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["l", "A", "r"])

    assert data == [("perm3", 39, 2, "visible2"), ("perm2", 30, 1, "visible"), 
                    ("perm1", 32, 0, ".hidden")]

    os.remove("tests/hidden.json")


def test_l_A_t():
    test_data = {
        "contents": [
            {"name": ".hidden", "size": 32, "time_modified": 1, 
             "permissions": "perm1"}, 
            {"name": "visible", "size": 33, "time_modified": 0, 
             "permissions": "perm2"},
            {"name": "visible2", "size": 38, "time_modified": 2, 
             "permissions": "perm3"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["l", "A", "t"])

    assert data == [("perm2", 33, 0, "visible"), ("perm1", 32, 1, ".hidden"), 
                    ("perm3", 38, 2, "visible2")]

    os.remove("tests/hidden.json")  


def test_l_t_r():
    test_data = {
        "contents": [
            {"name": ".hidden", "size": 32, "time_modified": 1, 
             "permissions": "perm1"}, 
            {"name": "visible", "size": 34, "time_modified": 0, 
             "permissions": "perm2"},
            {"name": "visible2", "size": 37, "time_modified": 2, 
             "permissions": "perm3"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["l", "t", "ls", "r"])

    assert data == [("perm3", 37,  2, "visible2"), ("perm2", 34, 0, "visible")]

    os.remove("tests/hidden.json")


def test_l_t_A_r():
    test_data = {
        "contents": [
            {"name": ".hidden", "size": 32, "time_modified": 1, 
             "permissions": "perm1"}, 
            {"name": "visible", "size": 33, "time_modified": 0, 
             "permissions": "perm2"},
            {"name": "visible2", "size": 30, "time_modified": 2, 
             "permissions": "perm3"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["l", "t", "A", "r"])

    assert data == [("perm3", 30, 2, "visible2"), ("perm1", 32, 1, ".hidden"), 
                    ("perm2", 33, 0, "visible")]

    os.remove("tests/hidden.json")


def test_r():
    test_data = {
        "contents": [
            {"name": ".hidden", "size": 32, "time_modified": 1, 
             "permissions": "perm1"}, 
            {"name": "visible", "size": 32, "time_modified": 0, 
             "permissions": "perm2"},
            {"name": "visible2", "size": 32, "time_modified": 2, 
             "permissions": "perm3"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["ls", "r"])

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


def test_l_t_r_filter_dir():
    test_data = {
        "contents": [
            {"name": ".hidden", "size": 30, "time_modified": 1, 
             "permissions": "perm1"}, 
            {"name": "visible", "size": 35, "time_modified": 0, 
             "permissions": "perm2"},
            {"name": "visible.go", "size": 31, "time_modified": 2, 
             "permissions": "perm3"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["l", "t", "ls", "r", "dir"])

    assert data == [("perm2", 35, 0, "visible")]

    os.remove("tests/hidden.json")


def test_l_t_r_filter_file():
    test_data = {
        "contents": [
            {"name": ".hidden", "size": 32, "time_modified": 1, 
             "permissions": "perm1"}, 
            {"name": "visible", "size": 32, "time_modified": 0, 
             "permissions": "perm2"},
            {"name": "visible.go", "size": 32, "time_modified": 2,
             "permissions": "perm3"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)

    data_files = parser_function("tests/hidden.json", ["l", "t", "ls", 
                                                       "r", "file"])

    assert data_files == [("perm3", 32, 2, "visible.go")]

    os.remove("tests/hidden.json")


def test_A_filter_file():
    test_data = {
        "contents": [
            {"name": "visible.go", "size": 30, "time_modified": 1, 
             "permissions": "perm1"}, 
            {"name": "README.hd", "size": 39, "time_modified": 0, 
             "permissions": "perm2"},
            {"name": "ast", "size": 32, "time_modified": 2, 
             "permissions": "perm3"},
            {"name": ".gitignore", "size": 29, "time_modified": 3, 
             "permissions": "perm4"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)
    data = parser_function("tests/hidden.json", ["A", "file"])

    assert data == ["visible.go", "README.hd", ".gitignore"]

    data_dir = parser_function("tests/hidden.json", ["A", "dir"])

    assert data_dir == ["ast"]

    os.remove("tests/hidden.json")


def test_l_navigate_folder():
    test_data = {
        "contents": [
            {
                "name": "folder", "size": 30, "time_modified": 1, 
                "permissions": "perm1", 
                "contents": [
                    {"name": "file1", "size": 32, "time_modified": 0, 
                     "permissions": "perm1"},
                    {"name": "file2", "size": 33, "time_modified": 1, 
                     "permissions": "perm1"}
                ]
            }, 
            {"name": "README.hd", "size": 39, "time_modified": 0, 
             "permissions": "perm2"},
            {
                "name": "ast", "size": 32, "time_modified": 2, 
                "permissions": "perm3", 
                "contents": [
                    {"name": "file3", "size": 32, "time_modified": 0, 
                     "permissions": "perm3"},
                    {"name": "file4", "size": 33, "time_modified": 1, 
                     "permissions": "perm3"}
                ]
            },
            {"name": ".gitignore", "size": 29, "time_modified": 3, 
             "permissions": "perm4"}
        ]
    }
    with open("tests/hidden.json", "w") as file:
        json.dump(test_data, file, indent=4)

    data = parser_function("tests/hidden.json", ["l", "navigate:ast"])

    assert data == [("perm3", 32, 0, "file3"), ("perm3", 33, 1, "file4")]

    os.remove("tests/hidden.json")


def test_navigate_path():
    test_data = {
        "name": "interpreter",
        "size": 4096,
        "time_modified": 1699957865,
        "permissions": "-rw-r--r--",
        "contents": [
            {
                "name": "LICENSE",
                "size": 1071,
                "time_modified": 1699941437,
                "permissions": "drwxr-xr-x"
            },
            {
                "name": "ast",
                "size": 4096,
                "time_modified": 1699957739,
                "permissions": "-rw-r--r--",
                "contents": [
                    {
                        "name": "go.mod",
                        "size": 225,
                        "time_modified": 1699957780,
                        "permissions": "-rw-r--r--"
                    },
                    {
                        "name": "go_test.mod",
                        "size": 250,
                        "time_modified": 1699957890,
                        "permissions": "-rw-r--r--"
                    }
                            ]
            }
                ]
                }
    returned = navigate_path("ast", test_data)

    assert returned == [("-rw-r--r--", 225, 1699957780, "go.mod"), 
                        ("-rw-r--r--", 250, 1699957890, "go_test.mod")]

    returned = navigate_path("ast/go.mod", test_data)

    assert returned == [("-rw-r--r--", 225, 1699957780, "go.mod")]


def test_navigate_invalid():
    test_data = {
        "name": "interpreter",
        "size": 4096,
        "time_modified": 1699957865,
        "permissions": "-rw-r--r--",
        "contents": [
            {
                "name": "LICENSE",
                "size": 1071,
                "time_modified": 1699941437,
                "permissions": "drwxr-xr-x"
            },
            {
                "name": "ast",
                "size": 4096,
                "time_modified": 1699957739,
                "permissions": "-rw-r--r--",
                "contents": [
                    {
                        "name": "go.mod",
                        "size": 225,
                        "time_modified": 1699957780,
                        "permissions": "-rw-r--r--"
                    },
                    {
                        "name": "go_test.mod",
                        "size": 250,
                        "time_modified": 1699957890,
                        "permissions": "-rw-r--r--"
                    }
                            ]
            }
                ]
                }
    with raises(ValueError, match="cannot access invalid: \
                No such file or directory"):
        _ = navigate_path("invalid", test_data)


def test_navigate_root():
    test_data = {
     "name": "interpreter",
     "size": 4096,
     "time_modified": 1699957865,
     "permissions": "-rw-r--r--",
     "contents": [
        {
            "name": "LICENSE",
            "size": 1071,
            "time_modified": 1699941437,
            "permissions": "drwxr-xr-x"
        },
        {
            "name": "ast",
            "size": 4096,
            "time_modified": 1699957739,
            "permissions": "-rw-r--r--",
            "contents": [
                {
                    "name": "go.mod",
                    "size": 225,
                    "time_modified": 1699957780,
                    "permissions": "-rw-r--r--"
                },
                {
                    "name": "go_test.mod",
                    "size": 250,
                    "time_modified": 1699957890,
                    "permissions": "-rw-r--r--"
                }
                        ]
        }
                ]
                }
    
    returned = navigate_path(".", test_data)

    assert returned == test_data

    

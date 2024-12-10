from typing import List
import json
from argparse import Namespace
import os

def parser_function(args: Namespace) -> None:
    if args is None:
        raise ValueError("args is required")
    if args.file == "":
        raise ValueError("file path is required")
    if os.path.exists(args.file) is False:
        raise ValueError("file does not exist")
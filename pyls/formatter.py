from typing import List
from argparse import Namespace

def formatter_function(args: Namespace, data: List) -> None:
    
    print(" ".join(data))
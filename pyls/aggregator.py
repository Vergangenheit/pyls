from argparse import Namespace
from typing import List

"""Function responsible for aggregating the option flags to that 
they are composable"""


def options_aggregator(args: Namespace) -> List[str]:
    options = []
    if args.open_option:
        options.append(f"navigate:{args.open_option}")
    if args.l:
        options.append("l")
        if args.A:
            options.append("A")
        else:
            options.append("ls")
    if args.t:
        if args.A:
            if "A" not in options:
                options.append("A")
        else:
            if "ls" not in options:
                options.append("ls")
        options.append("t")

    if args.r:
        if args.A:
            if "A" not in options:
                options.append("A")
        else:
            if "ls" not in options:
                options.append("ls")
        options.append("r")

    if args.filter:
        if args.A:
            if "A" not in options:
                options.append("A")
        else:
            if "ls" not in options:
                options.append("ls")
        options.append(args.filter)

    if len(options) == 0:
        if args.A:
            options.append("A")
        else:
            options.append("ls")
    
    return options
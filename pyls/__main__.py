from parser.parser import parser_function
from .formatter import formatter_function
import argparse

def main():
    argument_parser = argparse.ArgumentParser(description="parsing command line flags")

    argument_parser.add_argument("-file", help="json file path", type=str, required=False, default="structure.json")
    argument_parser.add_argument("-A", action="store_true", help="whether to print all contents", required=False)
    argument_parser.add_argument("-l", action="store_true", help="whether to print vertically with additional info", required=False)
    argument_parser.add_argument("-r", action="store_true", help="whether to print results in reverse", required=False)
    argument_parser.add_argument("-t", action="store_true", help="whether to sort results by time modified", required=False)

    args = argument_parser.parse_args()

    options = []
    
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
    if len(options) == 0:
        if args.A:
            options.append("A")
        else:
            options.append("ls")

    data = parser_function(args.file, options)

    formatter_function(data)

if __name__ == "__main__":
    main()
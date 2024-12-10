from parser.parser import parser_function
from .formatter import formatter_function
import argparse

def main():
    argument_parser = argparse.ArgumentParser(description="parsing command line flags")

    argument_parser.add_argument("-file", help="json file path", type=str, required=False, default="structure.json")
    argument_parser.add_argument("-A", action="store_true", help="whether to print all contents", required=False)

    args = argument_parser.parse_args()

    options = []
    if args.A:
        options.append("A")
    
    if len(options) == 0:
        options.append("ls")


    data = parser_function(args.file, options)

    formatter_function(data)

if __name__ == "__main__":
    main()
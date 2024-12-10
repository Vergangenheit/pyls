from parser.parser import parser_function
from .formatter import formatter_function
import argparse

def main():
    argument_parser = argparse.ArgumentParser(description="parsing command line flags")

    argument_parser.add_argument("-file", help="json file path", type=str, required=False, default="structure.json")

    args = argument_parser.parse_args()

    data = parser_function(args)

    formatter_function(args, data)

if __name__ == "__main__":
    main()
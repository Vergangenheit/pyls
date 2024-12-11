from parser.parser import parser_function
from .formatter import formatter_function
from .aggregator import options_aggregator
import argparse

def main():
    argument_parser = argparse.ArgumentParser(description="cli module that prints the contents of a filesystem directory from a json file",
                                              usage="python -m pyls [-h] [-file FILE] [-A] [-l] [-r] [-t] [--filter {dir,file}] [open_option]")

    argument_parser.add_argument("-file", help="json file path", type=str, required=False, default="structure.json")
    argument_parser.add_argument("-A", action="store_true", help="whether to print all contents", required=False)
    argument_parser.add_argument("-l", action="store_true", help="whether to print vertically with additional info", required=False)
    argument_parser.add_argument("-r", action="store_true", help="whether to print results in reverse", required=False)
    argument_parser.add_argument("-t", action="store_true", help="whether to sort results by time modified", required=False)
    argument_parser.add_argument("--filter", choices=["dir", "file"], type=str, help="whether to filter in dir or files", required=False)
    argument_parser.add_argument('open_option', type=str, nargs='?', help='Open option that accepts any single string \
                                 as long as it is a path of file within the json file')

    args = argument_parser.parse_args()
    
    options = options_aggregator(args)
    try:
        data = parser_function(args.file, options)
        formatter_function(data)
    except ValueError as e:
        print(f"error {e}")

if __name__ == "__main__":
    main()
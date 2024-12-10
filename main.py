

if __name__ == "__main__":
    from parser.parser import parser_function
    data = parser_function("structure.json", ["l", "t", "r"])
    print(f'Parsed data: {data}')
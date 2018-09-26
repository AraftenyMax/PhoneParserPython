from src.parser import Parser


if __name__ == "__main__":
    parser = Parser(config_name='allegro', extension='csv', quantity=5)
    parser.start_parse()
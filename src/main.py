from src.parser import Parser


if __name__ == "__main__":
    parser = Parser(config_name='allegro')
    parser.start_parse()
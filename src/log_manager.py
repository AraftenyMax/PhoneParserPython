from src.utils import get_base_folder_path, get_datetime_now


class LogManager:
    def __init__(self):
        self.filename = "{}/{}".format(get_base_folder_path(), 'logs/{}.txt'.format(get_datetime_now()))
        self.logfile = open(self.filename, 'a+')

    def on_init(self, config_name='', config={}, quantity=10,
                start_page=1, start_id=1, username='admin', extenstion='json'):
        self.logfile.write('Performing parse for: {}\n'.format(username))
        self.logfile.write('with quantity: {}, start page: {}, start_id: {}\n'.format(quantity, start_page, start_id))
        self.logfile.write('Own config: {}\n'.format(True if config else False))
        self.logfile.write('Config name: {}\n'.format(True if config_name else False))
        self.logfile.write('Response extension is {}\n'.format(extenstion))
        self.logfile.write('Started at: {}\n'.format(get_datetime_now()))

    def on_init_finish(self):
        self.logfile.write('Initialization: Success\n')

    def on_parse_start(self):
        self.logfile.write('Parsing: Start\n')

    def on_exception_occurred(self, e: Exception):
        self.logfile.write(str(e) + '\n')

    def on_parsing_finish(self):
        self.logfile.write('Parsing is finished at: {}\n'.format(get_datetime_now()))

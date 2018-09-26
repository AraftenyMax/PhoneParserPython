from src.utils import get_base_folder_path, get_datetime_now


class LogManager:
    def __init__(self):
        self.filename = "{}/{}.txt".format(get_base_folder_path(), get_datetime_now())
        self.logfile = open(self.filename, 'a+')

    def on_init(self, config_name='', config={}, quantity=10,
                start_page=1, start_id=1, username='admin', extenstion='json'):
        self.logfile.write('Performing parse for: {}'.format(username))
        self.logfile.write('with quantity: {}, start page: {}, start_id: {}'.format(quantity, start_page, start_id))
        self.logfile.write('Own config: {}'.format(True if config else False))
        self.logfile.write('Config name: {}'.format(True if config_name else False))
        self.logfile.write('Response extension is {}'.format(extenstion))
        self.logfile.write('Started at: {}'.format(get_datetime_now()))

    def on_init_finish(self):
        self.logfile.write('Initialization: Success')

    def on_parse_start(self):
        self.logfile.write('Parsing: Start')

    def on_exception_occurred(self, e: Exception):
        self.logfile.write(str(e))

    def on_parsing_finish(self):
        self.logfile.write('Parsing is finished at: {}'.format(get_datetime_now()))

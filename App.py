import os
import static
from collections import defaultdict
from InvertedListGenerator import InvertedListGenerator


class App(object):
    def __init__(self):
        self.logger = static.start_logger()

    def read_configuration_file(self, file):
        start_time = static.get_current_time()
        filename = os.path.basename(file)
        self.logger.info('Reading Configuration File %s' % filename)
        config = defaultdict(list)
        with open(file) as config_file:
            for line in config_file:
                key = line.rstrip().split('=')[0]
                value = line.rstrip().split('=')[1]
                config[key].append(value)
        static.log_execution_time('Reading Configuration File %s' % filename, self.logger, start_time)
        return config

    def generate_inverted_index(self):
        config = self.read_configuration_file('config/gli.cfg')
        inverted_list_generator = InvertedListGenerator(config, self.logger)
        inverted_list_generator.execute()

    def execute(self):
        start_time = static.get_current_time()
        self.logger.info('Starting BRI Exercise 1')
        self.generate_inverted_index()
        static.log_execution_time('BRI Exercise 1', self.logger, start_time)


app = App()
app.execute()

import os
import static
from collections import defaultdict
from Indexer import Indexer
from InvertedListGenerator import InvertedListGenerator


class App(object):
    def __init__(self):
        self.logger = static.start_logger()

    '''
    Eu tentei usar o módulo configparser, mas não encontrei nenhuma forma de fazê-lo 
    trabalhar com listas de opções em Python3 (como no gli.cfg, onde temos vários
    arquivos de entrada). Assim, preferi criar meu próprio leitor de configurações
    '''
    def read_configuration_file(self, file):
        start_time = static.get_current_time()
        filename = os.path.basename(file)
        self.logger.info('Reading Configuration File %s' % filename)
        config = defaultdict(list)
        with open(file) as config_file:
            for line in config_file:
                data = line.rstrip().split('=')
                config[data[0]].append(data[1])
        static.log_execution_time('Reading Configuration File %s' % filename, self.logger, start_time)
        return config

    def generate_inverted_index(self):
        config = self.read_configuration_file('config/gli.cfg')
        inverted_list_generator = InvertedListGenerator(config, self.logger)
        inverted_list_generator.execute()

    def index_model(self):
        config = self.read_configuration_file('config/index.cfg')
        indexer = Indexer(config, self.logger)
        indexer.execute()

    def execute(self):
        start_time = static.get_current_time()
        self.logger.info('Starting BRI Exercise 1')
        # self.generate_inverted_index()
        self.index_model()
        static.log_execution_time('BRI Exercise 1', self.logger, start_time)


app = App()
app.execute()

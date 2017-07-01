import ast
import csv
import static
from collections import defaultdict


class Indexer(object):
    def __init__(self, config, logger):
        self.logger = logger
        self.input = config.get('LEIA')
        self.output = config.get('ESCREVA')
        self.list = defaultdict(list)

    def read_inverted_list(self):
        start_time = static.get_current_time()
        self.logger.info('Reading inverted list')
        input_file = self.input[0]
        with open(input_file) as csv_file:
            field_names = ['word', 'documents']
            reader = csv.DictReader(csv_file, delimiter=';', lineterminator='\n', fieldnames=field_names)
            next(reader, None)  # skip the header - why do I need? Stupid system

            for line in reader:
                line_documents = ast.literal_eval(line['documents'])
                self.list[line['word']] = line_documents
        static.log_execution_time('Reading inverted list', self.logger, start_time)

    def build_model(self):
        start_time = static.get_current_time()
        self.logger.info('Generating vectorial model')

        static.log_execution_time('Generating vectorial model', self.logger, start_time)

    def execute(self):
        start_time = static.get_current_time()
        self.logger.info('Starting Indexer Module')
        self.read_inverted_list()
        self.build_model()
        static.log_execution_time('Indexer Module', self.logger, start_time)

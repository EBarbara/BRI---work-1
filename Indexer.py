import ast
import csv
import os
from collections import defaultdict

from math import log

import static


class Indexer(object):
    def __init__(self, config, logger):
        super(Indexer, self).__init__()
        self.logger = logger
        self.input_file = config.get('LEIA')[0]
        self.output_file = config.get('ESCREVA')[0]
        self.inverted_list = defaultdict(list)
        self.document_list = []
        self.model = {}

    def read_inverted_list(self):
        start_time = static.get_current_time()
        filename = os.path.basename(self.input_file)
        self.logger.info('Reading inverted list from file {0}'.format(filename))
        with open(self.input_file) as csv_file:
            field_names = ['word', 'documents']
            reader = csv.DictReader(csv_file, delimiter=';', lineterminator='\n', fieldnames=field_names)

            for line in reader:
                # Eliminando as palavras irrelevantes da lista invertida (palavras
                # com menos de duas letras ou contendo algo diferente de letras)
                if len(line['word']) > 2 and line['word'].isalpha():
                    line_documents = ast.literal_eval(line['documents'])
                    self.inverted_list[line['word']] = line_documents
                    self.document_list.extend(line_documents)
        self.document_list = list(set(self.document_list))
        static.log_execution_time('Reading inverted list from file {0}'.format(filename), self.logger, start_time)

    def build_model(self):
        start_time = static.get_current_time()
        self.logger.info('Generating vectorial model')
        # Enfim vamos começar a gerar o modelo
        for word, documents in self.inverted_list.items():
            documents_occurred = list(set(documents))
            idf = self.calculate_idf(documents_occurred)
            document_data = {}
            for document in documents_occurred:
                tf = self.calculate_tf(word, document)
                weight = tf * idf
                document_data[document] = weight
            self.model[word] = (idf, document_data)
        static.log_execution_time('Generating vectorial model', self.logger, start_time)

    def calculate_idf(self, documents_occurred):
        return log(len(self.document_list) / len(documents_occurred))

    def calculate_tf(self, word, document):
        return self.inverted_list[word].count(document)

    def write_model(self):
        start_time = static.get_current_time()
        filename = os.path.basename(self.output_file)
        self.logger.info('Writing Output File {0}'.format(filename))
        with open(self.output_file, 'w+') as csv_file:
            field_names = ['word', 'data']
            writer = csv.DictWriter(csv_file, delimiter=';', lineterminator='\n', fieldnames=field_names)
            for word in self.model:
                writer.writerow({'word': word, 'data': self.model[word]})
        static.log_execution_time('Writing Output File {0}'.format(filename), self.logger, start_time)

    def execute(self):
        start_time = static.get_current_time()
        self.logger.info('Starting Indexer Module')
        self.read_inverted_list()
        self.build_model()
        self.write_model()
        static.log_execution_time('Indexer Module', self.logger, start_time)

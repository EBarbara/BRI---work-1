import ast
import csv
import os
from collections import defaultdict
from math import log

import static


class Indexer(object):
    def __init__(self, config, logger):
        self.logger = logger
        self.input = config.get('LEIA')
        self.output = config.get('ESCREVA')
        self.inverted_list = defaultdict(list)
        self.document_list = []
        self.model = {}

    def read_inverted_list(self):
        start_time = static.get_current_time()
        input_file = self.input[0]
        filename = os.path.basename(input_file)
        self.logger.info('Reading inverted list from file {0}'.format(filename))
        with open(input_file) as csv_file:
            field_names = ['word', 'documents']
            reader = csv.DictReader(csv_file, delimiter=';', lineterminator='\n', fieldnames=field_names)
            next(reader, None)  # skip the header - since the lib doesn't know to do it automatically

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
            for document in documents_occurred:
                tf = self.calculate_tf(word, document)
                weight = tf * idf
                self.model[(word, document)] = weight
        static.log_execution_time('Generating vectorial model', self.logger, start_time)

    def calculate_idf(self, documents_occurred):
        return log(len(self.document_list) / len(documents_occurred))

    def calculate_tf(self, word, document):
        return self.inverted_list[word].count(document)

    def write_model(self):
        start_time = static.get_current_time()
        output_file = self.output[0]
        filename = os.path.basename(output_file)
        self.logger.info('Writing Output File {0}'.format(filename))
        with open(output_file, 'w+') as csv_file:
            field_names = ['word', 'document', 'weight']
            writer = csv.DictWriter(csv_file, delimiter=';', lineterminator='\n', fieldnames=field_names)
            writer.writeheader()
            for pair in self.model:
                writer.writerow({'word': pair[0], 'document': pair[1], 'weight': self.model[pair]})
        static.log_execution_time('Writing Output File {0}'.format(filename), self.logger, start_time)

    def execute(self):
        start_time = static.get_current_time()
        self.logger.info('Starting Indexer Module')
        self.read_inverted_list()
        self.build_model()
        self.write_model()
        static.log_execution_time('Indexer Module', self.logger, start_time)

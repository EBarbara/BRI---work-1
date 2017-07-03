import ast
import csv
import os
from collections import defaultdict, Counter
from math import log

import static


def calculate_max_frequency(document, word_frequency):
    max_frequency = 0
    for _, frequency in word_frequency.items():
        if document in frequency.keys():
            max_frequency = max(max_frequency, frequency[document])
    return max_frequency


class Indexer(object):
    def __init__(self, config, logger):
        super(Indexer, self).__init__()
        self.logger = logger
        self.input_file = config.get('LEIA')[0]
        self.output_file = config.get('ESCREVA')[0]
        self.inverted_list = defaultdict(list)
        self.document_list = []
        self.document_max = {}
        self.model = {}

    def read_inverted_list(self):
        start_time = static.get_current_time()
        filename = os.path.basename(self.input_file)
        self.logger.info('Reading inverted list from file {0}'.format(filename))
        word_frequency = {}
        with open(self.input_file) as csv_file:
            field_names = ['word', 'documents']
            reader = csv.DictReader(csv_file, delimiter=';', lineterminator='\n', fieldnames=field_names)

            for line in reader:
                # Eliminando as palavras irrelevantes da lista invertida (palavras
                # com menos de duas letras ou contendo algo diferente de letras)
                word = line['word']
                if len(word) > 2 and word.isalpha():
                    line_documents = ast.literal_eval(line['documents'])
                    self.inverted_list[word] = line_documents
                    self.document_list.extend(line_documents)
                    word_frequency.update({word: Counter(line_documents)})
        self.document_list = list(set(self.document_list))
        for document in self.document_list:
            self.document_max[document] = calculate_max_frequency(document, word_frequency)
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
                tf_n = self.normalize_tf(word, document)
                weight = tf_n * idf
                document_data[document] = weight
            self.model[word] = (idf, document_data)
        static.log_execution_time('Generating vectorial model', self.logger, start_time)

    def calculate_idf(self, documents_occurred):
        return log(len(self.document_list) / len(documents_occurred))

    def normalize_tf(self, word, document):
        tf = self.inverted_list[word].count(document)
        return tf/self.document_max[document]

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

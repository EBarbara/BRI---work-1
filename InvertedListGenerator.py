import csv
import os
import static
from collections import defaultdict
from lxml import etree
from nltk import word_tokenize


class InvertedListGenerator(object):
    def __init__(self, config, logger):
        super(InvertedListGenerator, self).__init__()
        self.logger = logger
        self.input = config.get('LEIA')
        self.output = config.get('ESCREVA')
        self.documents = dict()
        self.list = defaultdict(list)

    def read_documents(self):
        full_count = 0
        start_time = static.get_current_time()
        self.logger.info('Reading document abstracts')
        parser = etree.XMLParser(dtd_validation=True)
        for input_file in self.input:
            count = 0
            filename = os.path.basename(input_file)
            doc_time = static.get_current_time()
            self.logger.info('Reading Document File {0}'.format(filename))
            file = etree.parse(input_file, parser)
            for record in file.getroot().iterchildren():
                key = 'invalid'
                value = 'invalid'
                for element in record.iterchildren():
                    if element.tag == 'RECORDNUM':
                        key = int(element.text)
                    if element.tag == 'ABSTRACT' or element.tag == 'EXTRACT':
                        value = element.text
                if key != 'invalid':
                    if value != 'invalid':
                        self.documents[key] = word_tokenize(value)
                        count += 1
                    else:
                        self.logger.warn('Document {0} has no info'.format(key))
            static.log_execution_time('Reading Document File {0}'.format(filename), self.logger, doc_time)
            self.logger.info("Read {0} documents from {1}".format(count, filename))
            full_count += count
        static.log_execution_time('Reading document abstracts', self.logger, start_time)
        self.logger.info("Read {0} documents in total ".format(full_count))

    def generate_list(self):
        start_time = static.get_current_time()
        self.logger.info('Generating inverted list')

        for index, value in self.documents.items():
            for word in value:
                self.list[word.upper()].append(index)
        static.log_execution_time('Generating inverted list', self.logger, start_time)

    def write_list(self):
        start_time = static.get_current_time()
        output_file = self.output[0]
        filename = os.path.basename(output_file)
        self.logger.info('Writing Output File {0}'.format(filename))
        with open(output_file, 'w+') as csvfile:
            field_names = ['word', 'documents']
            writer = csv.DictWriter(csvfile, delimiter=';', lineterminator='\n', fieldnames=field_names)
            writer.writeheader()
            for word in self.list:
                writer.writerow({'word': word, 'documents': self.list[word]})
        static.log_execution_time('Reading Output File {0}'.format(filename), self.logger, start_time)

    def execute(self):
        start_time = static.get_current_time()
        self.logger.info('Starting Inverted List Generate Module')
        self.read_documents()
        self.generate_list()
        self.write_list()
        static.log_execution_time('Inverted List Generate Module', self.logger, start_time)

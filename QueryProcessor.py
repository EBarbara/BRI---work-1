import csv
import os
import static
from lxml import etree


def calculate_votes(score):
    result = 0
    while score:
        result += score % 10
        score //= 10
    return result


class QueryProcessor(object):
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.input_file = config.get('LEIA')[0]
        self.processed_queries_file = config.get('CONSULTAS')[0]
        self.expected_results_file = config.get('ESPERADOS')[0]
        self.raw_queries = None
        self.processed_queries = {}

    def read_raw_queries(self):
        start_time = static.get_current_time()
        filename = os.path.basename(self.input_file)
        self.logger.info('Reading raw query data from file {0}'.format(filename))
        parser = etree.XMLParser(dtd_validation=True)
        self.raw_queries = etree.parse(self.input_file, parser)
        static.log_execution_time('Reading raw query data from file {0}'.format(filename), self.logger, start_time)

    # Acho que reinventei a roda - esse dicionário de dicionários, quando impresso vira basicamente um JSON
    def process_queries(self):
        start_time = static.get_current_time()
        self.logger.info('Starting Processing queries')
        for raw_query in self.raw_queries.getroot().iterchildren():
            for element in raw_query.iterchildren():
                if element.tag == 'QueryNumber':
                    query_number = int(element.text)
                    self.processed_queries[query_number] = {}
                elif element.tag == 'QueryText':
                    query_text = element.text.replace('\n  ', '').replace('\n', '')
                    self.processed_queries[query_number]['text'] = query_text.upper()
                elif element.tag == 'Records':
                    self.processed_queries[query_number]['results'] = {}
                    for item in element.iterchildren():
                        document = int(item.text)
                        votes = calculate_votes(int(item.attrib.get("score")))
                        self.processed_queries[query_number]['results'][document] = calculate_votes(votes)
        static.log_execution_time('Processing queries', self.logger, start_time)

    def write_processed_queries(self):
        start_time = static.get_current_time()
        filename = os.path.basename(self.processed_queries_file)
        self.logger.info('Writing Processed Queries File {0}'.format(filename))
        with open(self.processed_queries_file, 'w+') as csv_file:
            field_names = ['query', 'words']
            writer = csv.DictWriter(csv_file, delimiter=';', lineterminator='\n', fieldnames=field_names)
            writer.writeheader()
            for query in self.processed_queries:
                writer.writerow({'query': query, 'words': self.processed_queries[query]['text']})
        static.log_execution_time('Writing Processed Queries File {0}'.format(filename), self.logger, start_time)

    def write_expected_results(self):
        start_time = static.get_current_time()
        filename = os.path.basename(self.expected_results_file)
        self.logger.info('Writing Expected Results File {0}'.format(filename))
        with open(self.expected_results_file, 'w+') as csv_file:
            field_names = ['query', 'document', 'votes']
            writer = csv.DictWriter(csv_file, delimiter=';', lineterminator='\n', fieldnames=field_names)
            writer.writeheader()
            for query in self.processed_queries:
                results = self.processed_queries[query]['results']
                for document in results:
                    writer.writerow({'query': query, 'document': document, 'votes': results[document]})
        static.log_execution_time('Writing Expected Results File {0}'.format(filename), self.logger, start_time)

    def execute(self):
        start_time = static.get_current_time()
        self.logger.info('Starting Query Processor Module')
        self.read_raw_queries()
        self.process_queries()
        self.write_processed_queries()
        self.write_expected_results()
        static.log_execution_time('Query Processor Module', self.logger, start_time)

import logging

import time


def start_logger():
    logger = logging.getLogger("BRI - Exercise 1")
    handler = logging.FileHandler('logs/BRI_1.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


class App(object):
    def __init__(self):
        self.logger = start_logger()

    def log_execution_time(self, title, start_time):
        finish_time = time.time()
        self.logger.info("Finish %s: %fs" % (title, finish_time - start_time))

    def generate_inverted_index(self):
        start_time = time.time()
        self.log_execution_time('Inverted List Generate Module', start_time)

    def execute(self):
        self.logger.info('Starting Workflow - BRI Exercise 1')
        self.generate_inverted_index()
        pass


app = App()
app.execute()

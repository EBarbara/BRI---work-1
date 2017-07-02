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


def log_execution_time(title, logger, start_time):
    finish_time = time.time()
    logger.info("Finish %s: %fs" % (title, finish_time - start_time))


def get_current_time():
    return time.time()


def calculate_votes(score):
    result = 0
    while score:
        result += score % 10
        score //= 10
    return result




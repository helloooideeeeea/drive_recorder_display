from loguru import logger
import random, string, os
import datetime


def root_dir():
    return os.getcwd()


def ymd():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d%')


def log_dir():
    return root_dir() + '/log/'


def get_logger():
    logger.add(f'{log_dir()}app_{ymd()}.log')
    return logger


def make_random_str(n=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


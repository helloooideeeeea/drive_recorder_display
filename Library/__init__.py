from loguru import logger
import random, string, os
import datetime


def root_dir():
    return os.getcwd()


def log_dir():
    return root_dir() + '/log/'


def data_dir():
    return root_dir() + '/data/'


def ymd():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d')


def ymdhm():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d%H%M')


def video_path(prefix):
    return data_dir() + prefix + '_' + ymdhm() + '.mp4'


def get_logger():
    logger.add(f'{log_dir()}app_{ymd()}.log')
    return logger


def make_random_str(n=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

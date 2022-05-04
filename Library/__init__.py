import random, string, os
import datetime
from dotenv import load_dotenv
load_dotenv()  # .env読込


def is_debug():
    return os.getenv('ENV') == "DEBUG"


def root_dir():
    return os.getcwd()


def log_dir():
    return root_dir() + '/log/'


def data_dir():
    return root_dir() + '/data/'


def inside_video_data_dir():
    return data_dir() + 'inside/'


def outside_video_data_dir():
    return data_dir() + 'outside/'


def assets_dir():
    return root_dir() + '/assets/'

def ymd():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d')


def ymdhm():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d%H%M')


def video_path(prefix):
    return data_dir() + prefix + '_' + ymdhm() + '.mp4'


def create_video_path(prefix):
    path = data_dir() + prefix + '/' + ymdhm()
    os.mkdir(path)
    return path + '/'

def make_random_str(n=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


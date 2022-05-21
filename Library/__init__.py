import random, string, os, glob
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


def jornal_log_path():
    return log_dir() + 'jornal_' + ymd() + '.log'


def video_path(prefix):
    return data_dir() + prefix + '_' + ymdhm() + '.avi'


def audio_path(prefix):
    return data_dir() + prefix + '_' + ymdhm() + '.mp3'


def create_video_path(prefix):
    path = data_dir() + prefix + '/' + ymdhm()

    os.makedirs(path, exist_ok=True)
    return path + '/'


def make_random_str(n=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def filter_able_path(search_dir, exclude_file_paths):
    files = glob.glob(search_dir + "*")
    for efp in exclude_file_paths:
        if efp in files:
            files.remove(efp)
    return files


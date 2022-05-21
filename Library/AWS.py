import boto3
import os
from loguru import logger
from multiprocessing import Process
from dotenv import load_dotenv

load_dotenv()  # .env読込


class Aws(object):
    LOG_DIR = "log"
    DATA_DIR = "data"

    upload_process_list = []

    def process_s3_upload_files(self, local_file_paths, dirname):
        for local_file_path in local_file_paths:
            proc = Process(target=Aws.s3_upload_file, args=[local_file_path, dirname])
            proc.start()
            self.upload_process_list.append(proc)

    @staticmethod
    def s3_upload_file(local_file_path, dirname):
        logger.info(f"s3 file upload start [{local_file_path}]")

        s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
                          aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
        file_name = os.path.basename(local_file_path)
        upload_path = 'drive_recorder/{}/{}'.format(dirname,file_name)
        s3.upload_file(local_file_path, os.getenv('UPLOAD_BUCKET'), upload_path)

        logger.info(f"s3 file upload end [{local_file_path}]")

        os.remove(local_file_path)

        logger.info(f"file delete {local_file_path}")

import time
from Library import app_log_path
from loguru import logger
from Library.UPS import UPS
from Library.Redis import Redis


def main():
    logger.add(app_log_path())
    redis = None
    try:
        redis = Redis()
        ups = UPS()
        counter = 0
        while True:
            version, vin, batcap, vout = ups.decode_uart()
            if vin == 'NG':
                counter += 1
            else:
                counter = 0
            if counter >= 3:
                break
            time.sleep(1)
    except:
        import traceback
        logger.error(traceback.print_exc())

    if redis is not None:
        # send message
        logger.info("ups external power supply disconnect!")
        redis.ups_publish()

if __name__ == "__main__":
    main()

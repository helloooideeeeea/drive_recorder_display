import time
from Library import log_dir, ymd
from loguru import logger
from Library.UPS import UPS
from Library.Redis import Redis


def main():
    logger.add(f'{log_dir()}watch_ups_{ymd()}.log')
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
                # send message
                redis.ups_publish()

            time.sleep(1)
    except:
        import traceback
        logger.error(traceback.print_exc())


if __name__ == "__main__":
    main()

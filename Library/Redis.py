import threading, os
from loguru import logger
import redis
from dotenv import load_dotenv
load_dotenv()  # .env読込


class Redis:

    UPS_CHANNEL_NAME = 'ups'
    UPS_REMOVE_EXTERNAL_POWER_SUPPLY_MESSAGE = 'remove'

    window = None
    redis_instance = None
    ups_subscribe_thread = None

    def __init__(self, window=None):
        self.window = window
        self.redis_instance = redis.StrictRedis(host=os.getenv("REDIS_HOST"), port=6379, db=0)

    def start_ups_subscribe(self):
        self.ups_subscribe_thread = threading.Thread(target=self.ups_subscribe)

    def stop_ups_subscribe(self):
        pass

    def ups_subscribe(self):
        ps = self.redis_instance.pubsub()
        ps.subscribe(self.UPS_CHANNEL_NAME)
        for message in ps.listen():
            if message["data"] == self.UPS_REMOVE_EXTERNAL_POWER_SUPPLY_MESSAGE:
                self.window.received_remove_external_power_supply_signal()

    def ups_publish(self):
        self.redis_instance.publish(self.UPS_CHANNEL_NAME, self.UPS_REMOVE_EXTERNAL_POWER_SUPPLY_MESSAGE)
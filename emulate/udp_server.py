import json
import os
import sys
import socket
import redis
import logging
import django
from time import sleep, time
from django.utils import timezone

logging.basicConfig(encoding='utf-8', level=logging.INFO)

redis_db = redis.Redis(
    host=os.environ.get('REDIS_HOST'),
    port=int(os.environ.get('REDIS_PORT', 0))
)

sys.path.insert(0, os.path.abspath('../backend'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'lights.settings'
django.setup()

from codes.models import Config


def current_milliseconds():
    return round(time() * 1000)


def reset_dmx_values():
    number_of_values = 5 * 28 * 3  # 5 rows, 28 columns, 3 color values
    serialized = ",".join("0" * number_of_values)
    redis_db.set('DMXvalues', serialized)


def start_udp_server():
    config = Config.objects.first()
    redis_db.set('DMXvalues_from_UDP_update_timestamp', current_milliseconds())
    udpServerSocket = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
    udpServerSocket.setblocking(0)
    udpServerSocket.bind(("0.0.0.0", int(os.environ.get('UDP_SERVER_PORT', 20002))))
    logging.info("Start UDP server")
    while True:
        try:
            bytesAddressPair = udpServerSocket.recvfrom(2048)

            message = bytesAddressPair[0]
            message = message.decode('utf-8')
            message = to_json(message)

            if message and str(message.get("key")) == str(config.udp_key):
                serialized = ",".join([str(x) for x in list(message["stage"])])
                redis_db.set('DMXvalues_from_UDP', serialized)
                redis_db.set('DMXvalues_from_UDP_update_timestamp', current_milliseconds())
        except Exception as e:
            pass
        config = Config.objects.first()

    reset_dmx_values()
    udpServerSocket.close()


def to_json(json_str):
    try:
        json_object = json.loads(json_str)
        return json_object
    except ValueError as e:
        return None


def main():
    while True:
        try:
            start_udp_server()
            sleep(1)
        except Exception as e:
            logging.warning('UDP server error ' + str(e))


if __name__ == '__main__':
    main()

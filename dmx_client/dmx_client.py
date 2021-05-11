import PyDMX
# https://github.com/YoshiRi/PyDMX
from dotenv import load_dotenv

import asyncio
import websockets
import os
import json
import numpy

load_dotenv()


class PyDMXMock:
	def __init__(self):
		self.d = [0] * 28 * 5 * 3

	def set_data(self, i, value):
		self.d[i] = value

	def send(self):
		print(f'{self.d}\n')


DEVICE_NAME = os.environ.get('DEVICE_NAME', '/dev/ttyUSB0')
DEBUG = os.environ.get('DEBUG') == 'True'

if DEBUG is False:
	dmx_device = PyDMX.PyDMX(DEVICE_NAME)
else:
	dmx_device = PyDMXMock()

SERVER_IP = os.environ.get('SERVER_IP', 'localhost')
SERVER_PORT = os.environ.get('WEBSOCKETS_SERVER_PORT', 5678)


async def handler():
	async with websockets.connect('ws://{}:{}'.format(SERVER_IP, SERVER_PORT)) as websocket:
		while True:
			message = await websocket.recv()

			dmx_values = message.split(',')
			number_dmx_channels_without_windows = 3*12
			dmx_values = dmx_values[number_dmx_channels_without_windows:]
			dmx_values = dmx_values[::-1]

			dmx_values = [max(0, min(int(x), 255)) for x in dmx_values]

			for i in range(0, len(dmx_values), 3):
				dmx_device.set_data(i+1, dmx_values[i+2])
				dmx_device.set_data(i+2, dmx_values[i+1])
				dmx_device.set_data(i+3, dmx_values[i+0])

			dmx_device.send()


asyncio.get_event_loop().run_until_complete(handler())


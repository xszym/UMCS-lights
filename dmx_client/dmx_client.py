import PyDMX
# https://github.com/YoshiRi/PyDMX
from dotenv import load_dotenv

import asyncio
import websockets
import os
import json
import numpy

load_dotenv()

DEVICE_NAME = '/dev/ttyUSB0'
# DEVICE_NAME = 'COM3'

dmx_device = PyDMX.PyDMX(DEVICE_NAME)

SERVER_IP = os.environ.get('SERVER_IP', 'localhost')
SERVER_PORT = os.environ.get('WEBSOCKETS_SERVER_PORT', 5678)


async def handler():
	async with websockets.connect('ws://{}:{}'.format(SERVER_IP, SERVER_PORT)) as websocket:
		while True:
			message = await websocket.recv()

			dmx_values = message.split(',')
			dmx_values = dmx_values[3*12:]
			dmx_values = dmx_values[::-1]
			# dmx_values.reverse()

			dmx_values = [max(0, min(int(x), 255)) for x in dmx_values]
			
			# print(dmx_values)
			# for index, value in enumerate(dmx_values):
			#	dmx_device.set_data(index+1, value)

			for i in range(0, len(dmx_values), 3):

				dmx_device.set_data(i+1, dmx_values[i+2])
				dmx_device.set_data(i+2, dmx_values[i+1])
				dmx_device.set_data(i+3, dmx_values[i+0])

			dmx_device.send()

asyncio.get_event_loop().run_until_complete(handler())


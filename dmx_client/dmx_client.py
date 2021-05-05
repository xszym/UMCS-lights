import PyDMX
# https://github.com/YoshiRi/PyDMX

import asyncio
import websockets
import os
import json
import numpy

# DEVICE_NAME = '/dev/ttyUSB0'
DEVICE_NAME = 'COM3'

dmx_device = PyDMX.PyDMX(DEVICE_NAME)

SERVER_IP = os.environ.get('SERVER_IP', 'localhost')
SERVER_PORT = os.environ.get('WEBSOCKETS_SERVER_PORT', 5678)


async def handler():
	async with websockets.connect(f'ws://{SERVER_IP}:{SERVER_PORT}') as websocket:
		while True:
			message = await websocket.recv()

			dmx_values = message.split(',')
			for index, value in enumerate(dmx_values):
				dmx_device.set_data(index+1, value)

			dmx_device.send()

asyncio.get_event_loop().run_until_complete(handler())


import asyncio
import websockets
import os

async def handler():
	async with websockets.connect('ws://localhost:' + os.environ.get('WEBSOCKETS_SERVER_PORT', '5678')) as websocket:
		while True:
			message = await websocket.recv()
			print(message)

asyncio.get_event_loop().run_until_complete(handler())

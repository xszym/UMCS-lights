import asyncio
import websockets

async def handler():
	async with websockets.connect('ws://localhost:5678') as websocket:
		while True:
			message = await websocket.recv()
			print(message)

asyncio.get_event_loop().run_until_complete(handler())

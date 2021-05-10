import asyncio
import websockets
import redis
import os

redis_db = redis.Redis(
	host=os.environ['REDIS_HOST'],
	port=int(os.environ['REDIS_PORT'])
)

async def send_dmx_values(websocket, path):
	while True:
		dmx_values = redis_db.get('DMXvalues').decode('utf-8')
		await websocket.send(dmx_values)
		await asyncio.sleep(100.0/1000.0)

start_server = websockets.serve(
	send_dmx_values,
	'0.0.0.0',
	int(os.environ['WEBSOCKETS_SERVER_PORT'])
)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

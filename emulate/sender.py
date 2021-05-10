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

		delay = 100.0/1000.0
		stop_sender = redis_db.get('stop_sender')
		if stop_sender is None or stop_sender.decode('utf-8') == str(True):
			delay = 2.0
		await asyncio.sleep(delay)
  

start_server = websockets.serve(
	send_dmx_values,
	'0.0.0.0',
	int(os.environ['WEBSOCKETS_SERVER_PORT'])
)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

import asyncio
import websockets
import redis
import os
from time import time


redis_db = redis.Redis(
	host=os.environ['REDIS_HOST'],
	port=int(os.environ['REDIS_PORT'])
)
FADE_IN_TIME_MILLISECONDS = 1000
FADE_OUT_TIME_MILLISECONDS = 1000


def current_milliseconds():
	return round(time() * 1000)


def get_fade_multiplier():
	now_time = current_milliseconds()
	code_start_time = int(redis_db.get('Code_start_time'))
	code_end_time = int(redis_db.get('Code_end_time'))
	
	multiplier = 1.0
	delta_from_start = now_time - code_start_time
	delta_to_end = code_end_time - now_time
	if delta_from_start < FADE_IN_TIME_MILLISECONDS:
		multiplier = delta_from_start / FADE_IN_TIME_MILLISECONDS
	elif delta_to_end < FADE_OUT_TIME_MILLISECONDS:
		multiplier = delta_to_end / FADE_OUT_TIME_MILLISECONDS
	return multiplier


def update_dmx_values_fade(dmx_values):
	multiplier = get_fade_multiplier()
	dmx_values = [min(255, max(0, int(int(x) * (multiplier)))) for x in dmx_values.split(",")]
	dmx_values = ",".join([str(e) for e in dmx_values])
	return dmx_values
	

async def send_dmx_values(websocket, path):
	while True:
		dmx_values = redis_db.get('DMXvalues').decode('utf-8')
		if dmx_values is None:
			continue

		dmx_values = update_dmx_values_fade(dmx_values)
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

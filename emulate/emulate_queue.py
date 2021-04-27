from subprocess import Popen, PIPE
from time import sleep, time
import redis

redis_db = redis.Redis(host='redis', port=6379)

def current_milliseconds():
	return round(time() * 1000)


WAIT_TIME = 30  # time to wait for code emulation in SECONDS
FRAME_TIMEOUT = 5000  # time to wait for a single frame before timeout in MILLISECONDS

# TODO - Download user code and pass it to process, as of right now it is hard-coded inside 'emulate.js'

process = Popen(['node', 'emulate.js'], stdout=PIPE)
redis_db.set("DMXvalues_update_timestamp", current_milliseconds())


for i in range(WAIT_TIME):
	ret = process.poll()

	if ret is not None:
		print(f"User code execution finished with code {ret}")
		break

	dmx_values = redis_db.get("DMXvalues")
	if dmx_values is None:
		print('DMXvalues is None', flush=True)
		sleep(1)
		continue
	print(f'DmxValues: {dmx_values}')

	last_update_time = redis_db.get("DMXvalues_update_timestamp")
	if last_update_time is None:
		print('last_update_time is None', flush=True)
		sleep(1)
		continue
	last_update_time = int(last_update_time.decode('utf-8'))

	time_now = current_milliseconds()
	delta = time_now - last_update_time

	if delta > FRAME_TIMEOUT:
		print('Frame timed out', flush=True)
		break

	sleep(1)

if process.poll() is None:
	print('Process timed out')
	process.kill()
else:
	print('Process finished')

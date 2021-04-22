
from subprocess import Popen, PIPE
from time import sleep, time
import datetime
import redis


redis_db = redis.Redis(host='redis', port=6379)

def current_milli_time():
	return round(time() * 1000)


WAIT_TIME = 30 # time to wait for code emulation in seconds
frame_timeout = 5000
# TODO - Download user code and pass it to process
process = Popen(['node', 'emulate.js'], stdout=PIPE)
redis_db.set("DMXvalues_update_timestamp", current_milli_time())

for i in range(WAIT_TIME):
	ret = process.poll()

	if ret is not None:
		print(f"User code execution finished with code {ret}")
		break

	dmx_values = redis_db.get("DMXvalues")
	print(f'DmxValues {dmx_values}')

	last_update_time = int(redis_db.get("DMXvalues_update_timestamp").decode('utf-8'))
	if last_update_time is None:
		print('last_update_time is None', flush=True)
		sleep(1)
		continue
	
	time_now = current_milli_time()
	delta = time_now - last_update_time
	print(f'delta: {delta}')

	if  delta > frame_timeout:
		print('frame timeout', flush=True)
		break

	print('sleeping one second')
	sleep(1)


print('OUT OF LOOP')
if process.poll() is None:
	print('KILLING')
	process.kill()

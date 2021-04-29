import os
import sys
import redis
import logging
from time import sleep, time
from subprocess import run as subprocess_run
from django.conf import settings


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

redis_db = redis.Redis(
	host=os.environ['REDIS_HOST'],
	port=int(os.environ['REDIS_PORT'])
)

settings.configure(
    DATABASE_ENGINE = 'django.db.backends.postgresql',
    DATABASE_NAME = os.environ.get('POSTGRES_DB', 'postgres'),
    DATABASE_USER = os.environ.get('POSTGRES_USER', 'postgres'),
    DATABASE_PASSWORD =  os.environ.get('POSTGRES_PASSWORD', 'postgres'),
    DATABASE_HOST = 'database',
    DATABASE_PORT = '5432',
    TIME_ZONE = 'UTC',
)

sys.path.insert(0, os.path.abspath('../'))
from backend.codes.models import Code


def current_milliseconds():
	return round(time() * 1000)


CODE_EMULATION_WAIT_TIME_SECONDS = 30
FRAME_TIMEOUT_MILLISECONDS = 5000


class FrameTimeoutException(BaseException):
	"""Exception when frame timeout"""


class UserCodeException(BaseException):
	"""Exception when start user code"""


def check_process(process) -> None:
	ret = process.poll()

	if ret is not None:
		raise UserCodeException


def check_redis_dmx() -> None:
	dmx_values = redis_db.get('DMXvalues')
	if dmx_values is None:
		return

	last_update_time = redis_db.get('DMXvalues_update_timestamp')
	if last_update_time is None:
		return

	last_update_time = int(last_update_time.decode('utf-8'))

	time_now = current_milliseconds()
	delta = time_now - last_update_time

	if delta > FRAME_TIMEOUT_MILLISECONDS:
		raise FrameTimeoutException


def start_process(code: str):
	process = subprocess_run(['node', 'emulate_redis.js'], input=code, encoding='utf-8')
	redis_db.set('DMXvalues_update_timestamp', current_milliseconds())
	return process


def wait_for_emulation(process, duration_of_emulation_in_seconds) -> None:
	for i in range(duration_of_emulation_in_seconds):
		try:
			check_process(process)
			check_redis_dmx()
		except FrameTimeoutException:
			logging.warning('FrameTimeoutException')
			break
		except UserCodeException:
			logging.warning('UserCodeException')
			break

		sleep(1)


def run_code(code: str, duration_of_emulation_in_seconds: int) -> None:
	process = start_process(code)
	wait_for_emulation(process, duration_of_emulation_in_seconds)
	return_process_poll = process.poll()

	if return_process_poll is None:
		logging.warning('Process timed out')
		logging.warning('Killing process')
		process.kill()
	else:
		logging.info(f'Process finished with return code {return_process_poll}')


def retrieve_next_code() -> str:
	
	# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
	# https://stackoverflow.com/questions/2180415/using-django-database-layer-outside-of-django

	pass


def main():
	while True:
		logging.info(f'Running code for {CODE_EMULATION_WAIT_TIME_SECONDS} seconds')

		code = """
		let v = 0;

		async function loop() {
			for (let i = 0; i < 5; i++) {
				for (let j = 0; j < 28; j++) {
					values[i][j] = [v, v, v]
				}
			}
			v += 1;
			if (v > 255) v = 0;
			NextFrame(values)
			await sleep(1000)
		}
		"""
		
		run_code(code, CODE_EMULATION_WAIT_TIME_SECONDS)


if __name__ == '__main__':
	main()

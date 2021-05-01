import os
import sys
import redis
import logging
from time import sleep, time
from subprocess import run as subprocess_run
import django
import random


logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

redis_db = redis.Redis(
	host=os.environ['REDIS_HOST'],
	port=int(os.environ['REDIS_PORT'])
)

sys.path.insert(0, os.path.abspath('../backend'))

# https://stackoverflow.com/questions/4383571/importing-files-from-different-folder
# https://stackoverflow.com/questions/2180415/using-django-database-layer-outside-of-django

os.environ['DJANGO_SETTINGS_MODULE'] = 'lights.settings'
django.setup()

from codes.models import Code


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
	logging.info('Checking redis dmx...')

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
		logging.info(f'{i}: Checking process ...')
		try:
			check_process(process)
			check_redis_dmx()
		except FrameTimeoutException:
			logging.warning('FrameTimeoutException')
			break
		except UserCodeException:
			logging.warning('UserCodeException')
			break

		logging.info('Sleeping 1s ..')
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


def retrieve_next_animation() -> Code:
	pk_list = Code.objects.filter(approved=True).values_list('pk', flat=True)
	random_pk = random.choice(pk_list)
	return Code.objects.get(pk=random_pk)


def main():
	while True:
		logging.info(f'Running code for {CODE_EMULATION_WAIT_TIME_SECONDS} seconds')

		animation = retrieve_next_animation()
		logging.info(f'Animation name: {animation.name}')

		run_code(animation.code, CODE_EMULATION_WAIT_TIME_SECONDS)


if __name__ == '__main__':
	main()

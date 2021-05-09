import os
import sys
import redis
import logging
import django
import random
import subprocess
from time import sleep, time
from datetime import datetime

logging.basicConfig(encoding='utf-8', level=logging.WARNING)

redis_db = redis.Redis(
	host=os.environ['REDIS_HOST'],
	port=int(os.environ['REDIS_PORT'])
)

sys.path.insert(0, os.path.abspath('../backend'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'lights.settings'
django.setup()

from codes.models import Code
from codes.models import Config


def current_milliseconds():
	return round(time() * 1000)


CODE_EMULATION_WAIT_TIME_SECONDS = 30
FRAME_TIMEOUT_MILLISECONDS = 5000


class FrameTimeoutException(BaseException):
	"""Exception when frame timeout"""


class UserCodeException(BaseException):
	"""Exception when start user code"""


class NoCodeInDatabaseException(BaseException):
	"""Exception when there is no code in databae"""


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


def save_to_tmp_file(code: str) -> None:
	with open('tmp', 'wb') as file:
		file.write(code.encode('utf-8'))


def start_process(code: str):
	save_to_tmp_file(code)
	process = subprocess.Popen(['node', 'emulate_redis.js'])
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
	if len(pk_list) == 0:
		raise NoCodeInDatabaseException
	random_pk = random.choice(pk_list)
	return Code.objects.get(pk=random_pk)

def is_time_between(begin_time, end_time, check_time=None):
	# If check time is not given, default to current time
	check_time = check_time or datetime.now().time()
	if begin_time < end_time:
		return check_time >= begin_time and check_time <= end_time
	else: # crosses midnight
		return check_time >= begin_time or check_time <= end_time

def should_animate() -> bool:
	""" returns if an animation should be shown based on db config """
	cfg = Config.objects.first()
	if cfg is None:
		return True
	if cfg.force_stop is True:
		return False
	if cfg.force_run is True:
		return True
	if cfg.animation_start_time is None or cfg.animation_end_time is None:
		return True
	return is_time_between(cfg.animation_start_time, cfg.animation_end_time)


def main():
	while True:
		logging.info(f'Running code for {CODE_EMULATION_WAIT_TIME_SECONDS} seconds')
		if not should_animate():
			sleep(2)
			continue

		try:
			animation = retrieve_next_animation()
			logging.info(f'Animation name: {animation.name}')

			run_code(animation.code, CODE_EMULATION_WAIT_TIME_SECONDS)
		except NoCodeInDatabaseException:
			logging.warning('No Code In Database')
			sleep(1)


if __name__ == '__main__':
	main()

import json
import os
import sys
import socket
import redis
import logging
import django
import random
import subprocess
import threading
from time import sleep, time
from django.utils import timezone

logging.basicConfig(encoding='utf-8', level=logging.WARNING)

redis_db = redis.Redis(
	host=os.environ.get('REDIS_HOST'),
	port=int(os.environ.get('REDIS_PORT', 0))
)

sys.path.insert(0, os.path.abspath('../backend'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'lights.settings'
django.setup()

from codes.models import Code, Config, AnimationPriorityQueueElement


def current_milliseconds():
	return round(time() * 1000)


FRAME_TIMEOUT_MILLISECONDS = 5000


class FrameTimeoutException(BaseException):
	"""Exception when frame timeout"""


class UserCodeException(BaseException):
	"""Exception when start user code"""


class NoCodeInDatabaseException(BaseException):
	"""Exception when there is no code in database"""


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


def start_process(code: str, duration_of_emulation_in_seconds: int):
	save_to_tmp_file(code)
	process = subprocess.Popen(['node', 'emulate_redis.js'])
	redis_db.set('DMXvalues_update_timestamp', current_milliseconds())
	redis_db.set('Code_start_time', current_milliseconds())
	redis_db.set('Code_end_time', current_milliseconds() + duration_of_emulation_in_seconds*1000)
	return process


def is_time_between(begin_time, end_time, check_time=None) -> bool:
	check_time = check_time or timezone.now().time()
	if begin_time < end_time:
		return begin_time <= check_time <= end_time
	else: # crosses midnight
		return check_time >= begin_time or check_time <= end_time


def should_animate() -> bool:
	cfg = Config.objects.first()
	if cfg is None:
		return True
	if cfg.force_stop is True:
		return False
	if cfg.force_run is True:
		return True
	if cfg.animation_start_time is None or cfg.animation_end_time is None:
		return True
	if cfg.udp_receive_run is True:
		return False
	return is_time_between(cfg.animation_start_time, cfg.animation_end_time)


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

		if not should_animate():
			logging.info('Finishing animation early ..')
			return
		logging.info('Sleeping 1s ..')
		sleep(1)


def run_code(code: str, duration_of_emulation_in_seconds: int) -> None:
	process = start_process(code, duration_of_emulation_in_seconds)

	wait_for_emulation(process, duration_of_emulation_in_seconds)
	return_code = process.poll()

	if return_code is None:
		logging.warning('Process timed out')
		logging.warning('Killing process')
		process.kill()
	elif return_code == 0:
		logging.info(f'Process finished properly')
	else:
		logging.info(f'Process finished with return code {return_code}')
		raise UserCodeException


def retrieve_animation_from_priority_queue() -> Code:
	if (priority_queue := AnimationPriorityQueueElement.objects.order_by('-priority').first()):
		priority_code = priority_queue.code
		priority_queue.delete()
		return priority_code
	return None


def retrieve_random_animation() -> Code:
	pk_list = Code.objects.filter(approved=True).values_list('pk', flat=True)
	if len(pk_list) == 0:
		raise NoCodeInDatabaseException
	random_pk = random.choice(pk_list)
	return Code.objects.get(pk=random_pk)


def retrieve_next_animation() -> Code:
	code_from_priority_queue = retrieve_animation_from_priority_queue()
	if code_from_priority_queue is not None:
		return code_from_priority_queue
	return retrieve_random_animation()


def reset_dmx_values():
	number_of_values = 5 * 28 * 3  # 5 rows, 28 columns, 3 color values
	serialized = ",".join("0" * number_of_values)
	redis_db.set('DMXvalues', serialized)


def get_dmx_values_from_udp_server():
	last_udp_server_update_millis = current_milliseconds()
	config = Config.objects.first()
	while config.udp_receive_run:
		try:
			dmx_values_from_UDP = redis_db.get('DMXvalues_from_UDP').decode('utf-8')
			redis_db.set('DMXvalues', dmx_values_from_UDP)
			redis_db.set('Code_end_time', current_milliseconds() + 60000)
		except Exception as e:
			logging.warning(e)
		
		last_udp_server_update_millis = int(redis_db.get('DMXvalues_from_UDP_update_timestamp').decode('utf-8'))

		if (current_milliseconds() - last_udp_server_update_millis) > 60000:
			config.udp_receive_run = False
			config.save()
			break
		config = Config.objects.first()

	reset_dmx_values()


def to_json(json_str):
    try:
        json_object = json.loads(json_str)
        return json_object
    except ValueError as e:
        return None


def main():
	while True:
		if not should_animate():
			reset_dmx_values()
			redis_db.set('stop_sender', str(True))
			sleep(2)
			continue
		redis_db.set('stop_sender', str(False))

		try:
			get_dmx_values_from_udp_server()
		except Exception as e:
			logging.warning('Error when getting values from UDP server ' + str(e))
			conf = Config.objects.first()
			conf.udp_receive_run = False
			conf.save()

		try:
			animation = retrieve_next_animation()
			logging.info(f'Running code for {animation.duration_of_emulation_in_seconds} seconds')
			logging.info(f'Animation name: {animation.name}')

			run_code(animation.code, animation.duration_of_emulation_in_seconds)

		except UserCodeException:
			logging.warning('User animation generated error')
			animation.generated_error = True
			animation.approved = False
			animation.date_approved = None
			animation.save()
		except NoCodeInDatabaseException:
			logging.warning('No Code In Database')
			sleep(1)


if __name__ == '__main__':
	main()

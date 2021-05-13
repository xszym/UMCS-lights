import subprocess

import emulate_queue


class MockProcess:
    def __init__(self, return_value):
        self.return_value = return_value

    def poll(self):
        return self.return_value


def test_hello(get_hello):
    assert get_hello == 'hello'


def test_check_process_returns_none():
    assert emulate_queue.check_process(MockProcess(None)) is None


def test_check_process_returns_process_output():
    try:
        emulate_queue.check_process(MockProcess(0))
    except emulate_queue.UserCodeException:
        assert True
    else:
        assert False


def test_start_process(monkeypatch, redis_client):
    code_test = 'testCode'
    milliseconds = 1000

    def mock_save_to_tmp_file(code):
        assert code == code_test

    def mock_popen(values):
        assert values == ['node', 'emulate_redis.js']
        return None

    def mock_milliseconds():
        return milliseconds

    monkeypatch.setattr(emulate_queue, 'save_to_tmp_file', mock_save_to_tmp_file)
    monkeypatch.setattr(emulate_queue, 'current_milliseconds', mock_milliseconds)
    monkeypatch.setattr(subprocess, 'Popen', mock_popen)

    process = emulate_queue.start_process(code_test, 30)

    value = redis_client.get('DMXvalues_update_timestamp').decode('utf-8')
    assert value == str(milliseconds)
    assert process is None

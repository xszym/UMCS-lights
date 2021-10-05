import pytest
from redis import Redis
from pytest_mock_resources import create_redis_fixture

import emulate_queue

redis = create_redis_fixture()


@pytest.fixture()
def get_hello():
    return 'hello'


@pytest.fixture()
def redis_client(monkeypatch, redis):
    client = Redis(**redis.pmr_credentials.as_redis_kwargs())
    monkeypatch.setattr(emulate_queue, 'redis_db', redis)
    return client

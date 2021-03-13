import json
from django.urls import reverse
from rest_framework import status


def test_hello_world():
    assert "hello_world" == "hello_world"
    assert "foo" != "bar"


def test_ping(client):
    url = reverse('ping')
    response = client.get(url)
    content = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert content['ping'] == 'pong!'

import pytest
from django.urls import reverse
from rest_framework import status

from tests import factories
from codes.models import Code


@pytest.mark.django_db
@pytest.mark.parametrize('data',
    [
        {'name': 'TestCorrect', 'author': 'Maciej', 'code': 'print(1)'},
        {'name': 'SomeWeirdField', 'SomeWeirdField': 'SomeWeirdValue', 'author': 'Maciej', 'code': 'print(1)'},
        {'name': 'MultilineCodeLF', 'author': 'Mateusz', 'code': '\n\nprint(1)\nprint(2)\n'},
        {'name': 'MultilineCodeCRLF', 'author': 'Mateusz', 'code': '\r\n\r\nprint(1)\r\nprint(2)\r\n'},
    ]
)
def test_add_code_created(client, data):
    url = reverse('code-list')
    response = client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == data['name']
    assert Code.objects.count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize('data',
    [
        {'name': '', 'author': 'Mateusz', 'code': 'print(1)'},
        {'author': 'Mateusz', 'code': 'print(1)'},
        {'name': 'TestEmptyCode', 'author': 'Mateusz', 'code': ''},
        {'name': 'TestEmptyCode', 'author': 'Mateusz'},
        {'name': 'TestEmptyAuthor', 'author': '', 'code': 'print(1)'},
        {'name': 'TestEmptyAuthor', 'code': 'print(1)'},
        {'name': '', 'author': '', 'code': ''},
        {},
        {'name': '\0', 'author': 'Maciej', 'code': 'print(1)'},
        {'name': 'AuthorWithNull', 'author': '\0', 'code': 'print(1)'},
        {'name': 'CodeWithNull', 'author': 'Mateusz', 'code': '\0'},
    ]
)
def test_add_code_bad_request(client, data):
    url = reverse('code-list')
    response = client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Code.objects.count() == 0

@pytest.mark.django_db
def test_add_code_invalid_json(client):
    url = reverse('code-list')
    response = client.post(
        url,
        {}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_single_code(client):
    code = factories.CodeFactory.create(is_example=True)
    assert Code.objects.count() == 1

    url = reverse('code-detail', args=(code.pk,))
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_single_code_no_example(client):
    code = factories.CodeFactory.create(is_example=False)

    url = reverse('code-detail', args=(code.pk,))
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND

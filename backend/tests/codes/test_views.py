import pytest
from django.urls import reverse
from rest_framework import status

from tests import factories
from codes.models import Code


@pytest.mark.django_db
@pytest.mark.parametrize('data,expected_status,expected_object_count',
    [
        ({'name': 'TestCorrect', 'author': 'Maciej', 'code': 'print(1)'}, status.HTTP_201_CREATED, 1),
        ({'name': 'SomeWeirdField', 'SomeWeirdField': 'SomeWeirdValue', 'author': 'Maciej', 'code': 'print(1)'}, status.HTTP_201_CREATED, 1),
        ({'name': 'MultilineCodeLF', 'author': 'Mateusz', 'code': '\n\nprint(1)\nprint(2)\n'}, status.HTTP_201_CREATED, 1),
        ({'name': 'MultilineCodeCRLF', 'author': 'Mateusz', 'code': '\r\n\r\nprint(1)\r\nprint(2)\r\n'}, status.HTTP_201_CREATED, 1),
        ({'name': '', 'author': 'Mateusz', 'code': 'print(1)'}, status.HTTP_400_BAD_REQUEST, 0),
        ({'author': 'Mateusz', 'code': 'print(1)'}, status.HTTP_400_BAD_REQUEST, 0),
        ({'name': 'TestEmptyCode', 'author': 'Mateusz', 'code': ''}, status.HTTP_400_BAD_REQUEST, 0),
        ({'name': 'TestEmptyCode', 'author': 'Mateusz'}, status.HTTP_400_BAD_REQUEST, 0),
        ({'name': 'TestEmptyAuthor', 'author': '', 'code': 'print(1)'}, status.HTTP_400_BAD_REQUEST, 0),
        ({'name': 'TestEmptyAuthor', 'code': 'print(1)'}, status.HTTP_400_BAD_REQUEST, 0),
        ({'name': '', 'author': '', 'code': ''}, status.HTTP_400_BAD_REQUEST, 0),
        ({}, status.HTTP_400_BAD_REQUEST, 0),
        ({'name': '\0', 'author': 'Maciej', 'code': 'print(1)'}, status.HTTP_400_BAD_REQUEST, 0),
        ({'name': 'NameWithNull\0', 'author': 'Maciej', 'code': 'print(1)'}, status.HTTP_400_BAD_REQUEST, 0),
        ({'name': 'NameWith\0Null', 'author': 'Maciej', 'code': 'print(1)'}, status.HTTP_400_BAD_REQUEST, 0),
        ({'name': 'AuthorWithNull', 'author': '\0', 'code': 'print(1)'}, status.HTTP_400_BAD_REQUEST, 0),
        ({'name': 'AuthorWithNull', 'author': 'Mateusz\0', 'code': 'print(1)'}, status.HTTP_400_BAD_REQUEST, 0),
        ({'name': 'AuthorWithNull', 'author': 'Mate\0sz', 'code': 'print(1)'}, status.HTTP_400_BAD_REQUEST, 0),
        ({'name': 'CodeWithNull', 'author': 'Mateusz', 'code': '\0'}, status.HTTP_400_BAD_REQUEST, 0),
        ({'name': 'CodeWithNull', 'author': 'Mateusz', 'code': 'print(1)\0'}, status.HTTP_400_BAD_REQUEST, 0),
        ({'name': 'CodeWithNull', 'author': 'Mateusz', 'code': 'print(\0)'}, status.HTTP_400_BAD_REQUEST, 0),
    ]
)
def test_add_code(client, data, expected_status, expected_object_count):
    url = reverse('code-list')
    response = client.post(url, data)

    assert response.status_code == expected_status
    if response.status_code == status.HTTP_201_CREATED:
        assert response.data['name'] == data['name']
    assert Code.objects.count() == expected_object_count


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

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
    url = reverse('codes-list')
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
    url = reverse('codes-list')
    response = client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Code.objects.count() == 0

@pytest.mark.django_db
def test_add_code_invalid_json(client):
    url = reverse('codes-list')
    response = client.post(
        url,
        {}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_single_code(client):
    code = factories.CodeFactory.create(is_example=True)
    assert Code.objects.count() == 1

    url = reverse('codes-detail', args=(code.pk,))
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_single_code_no_example_filtering_by_example_true(client):
    code = factories.CodeFactory.create(is_example=False)

    url = reverse('codes-detail', args=(code.pk,))
    response = client.get(url, {'example': True})

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_codes_list(client):
    number_of_example_codes = 4
    list_of_codes = factories.CodeFactory.create_batch(number_of_example_codes, is_example=True)

    url = reverse('codes-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == number_of_example_codes


@pytest.mark.django_db
def test_get_codes_list_no_examples_filtering_by_example_true(client):
    number_of_example_codes = 4
    list_of_codes = factories.CodeFactory.create_batch(number_of_example_codes, is_example=False)

    url = reverse('codes-list')
    response = client.get(url, {'example': True})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.django_db
def test_get_codes_list_mixed_filtering_by_example_true(client):
    number_of_example_codes = 4
    number_of_no_example_codes = 2
    list_of_codes_example = factories.CodeFactory.create_batch(number_of_example_codes, is_example=True)
    list_of_codes_no_example = factories.CodeFactory.create_batch(number_of_no_example_codes, is_example=False)

    url = reverse('codes-list')
    response = client.get(url, {'example': True})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == number_of_example_codes


@pytest.mark.django_db
def test_get_codes_list_big_number_of_codes(client):
    number_of_example_codes = 1000
    list_of_codes = factories.CodeFactory.create_batch(number_of_example_codes, is_example=True)

    url = reverse('codes-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == number_of_example_codes


@pytest.mark.django_db
def test_get_single_approved_code(client):
    code = factories.CodeFactory.create(approved=True)
    assert Code.objects.count() == 1

    url = reverse('codes-detail', args=(code.pk,))
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK



@pytest.mark.django_db
def test_get_single_code_no_approved_filtering_by_approved_true(client):
    code = factories.CodeFactory.create(approved=False)

    url = reverse('codes-detail', args=(code.pk,))
    response = client.get(url, {'approved': True})

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_approved_codes_list(client):
    number_of_approved_codes = 4
    list_of_codes = factories.CodeFactory.create_batch(number_of_approved_codes, approved=True)

    url = reverse('codes-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == number_of_approved_codes


@pytest.mark.django_db
def test_get_codes_list_no_approved_filtering_by_approved_true(client):
    number_of_approved_codes = 4
    list_of_codes = factories.CodeFactory.create_batch(number_of_approved_codes, approved=False)

    url = reverse('codes-list')
    response = client.get(url, {'approved': True})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.django_db
def test_get_codes_list_mixed_filtering_by_example_true(client):
    number_of_approved_codes = 4
    number_of_not_approved_codes = 2
    list_of_codes_approved = factories.CodeFactory.create_batch(number_of_approved_codes, approved=True)
    list_of_codes_not_approved = factories.CodeFactory.create_batch(number_of_not_approved_codes, approved=False)

    url = reverse('codes-list')
    response = client.get(url, {'approved': True})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == number_of_approved_codes


@pytest.mark.django_db
def test_get_codes_list_big_number_of_codes(client):
    number_of_approved_codes = 1000
    list_of_codes = factories.CodeFactory.create_batch(number_of_approved_codes, approved=True)

    url = reverse('codes-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == number_of_approved_codes


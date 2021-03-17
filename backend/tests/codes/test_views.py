import pytest
from django.urls import reverse
from rest_framework import status

from tests import factories
from codes.models import Code


@pytest.mark.django_db
def test_add_code(client):
    url = reverse('code-list')
    response = client.post(
        url,
        {
            'name': 'Test',
            'author': 'maciej',
            'code': 'print(1)',
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == 'Test'
    assert Code.objects.count() == 1


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

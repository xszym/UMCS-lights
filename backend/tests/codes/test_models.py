import pytest
import logging

from tests import factories
from codes.models import Code


LOGGER = logging.getLogger(__name__)


@pytest.mark.django_db
def test_code_model():
    code = Code(name='TestCode', author='maciej', description='example', code='print("Hello world")')
    code.save()

    assert code.name == 'TestCode'


@pytest.mark.django_db
def test_code_factory():
    factories.CodeFactory.create_batch(10)

    assert Code.objects.count() == 10

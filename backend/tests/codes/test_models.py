import pytest
import logging

from tests import factories
from codes.models import Code, Config, AnimationPriorityQueueElement


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


@pytest.mark.django_db
def test_config_model():
    config = Config(force_run=False, force_stop=False)
    config.save()

    assert Config.objects.count() == 1
    assert config.force_run == False
    

@pytest.mark.django_db
def test_config_model_save_multiple():
    try:
        factories.ConfigFactory.create_batch(3)
        assert False
    except django.db.utils.IntegrityError:
        assert True


@pytest.mark.django_db
def test_priority_queue_model():
    example_code = factories.CodeFactory.create()
    priority_queue_element = AnimationPriorityQueueElement(code=example_code, priority=10)
    priority_queue_element.save()

    returned_element = AnimationPriorityQueueElement.pop_first()
    
    assert AnimationPriorityQueueElement.objects.count() == 0
    assert returned_element.priority == priority_queue_element.priority


@pytest.mark.django_db
def test_priority_queue_model():
    example_code = factories.CodeFactory.create()
    priority_queue_element = AnimationPriorityQueueElement(code=example_code, priority=10)
    priority_queue_element.save()

    
    assert AnimationPriorityQueueElement.objects.count() == 1


@pytest.mark.django_db
def test_priority_queue_model_mulitiple_objects():
    factories.AnimationPriorityQueueElementFactory.create_batch(10)

    
    assert AnimationPriorityQueueElement.objects.count() == 10


@pytest.mark.django_db
def test_priority_queue_model_mulitiple_objects_pop_first():
    factories.AnimationPriorityQueueElementFactory.create_batch(10)
    AnimationPriorityQueueElement.pop_first()
    
    assert AnimationPriorityQueueElement.objects.count() == 9


@pytest.mark.django_db
def test_priority_queue_model_return_higher_priority():
    example_code1 = factories.CodeFactory.create()
    example_code2 = factories.CodeFactory.create()
    priority_queue_high_priority_element = factories.AnimationPriorityQueueElementFactory(code=example_code1, priority = 6)
    priority_queue_high_priority_element.save()
    priority_queue_low_priority_element = AnimationPriorityQueueElement(code=example_code2, priority = 3)
    priority_queue_low_priority_element.save()
    
    returned_element = AnimationPriorityQueueElement.pop_first() 

    assert AnimationPriorityQueueElement.objects.count() == 1
    assert returned_element.pk == priority_queue_high_priority_element.pk


@pytest.mark.django_db
def test_priority_queue_model_return_highest_priority():
    factories.AnimationPriorityQueueElementFactory.create_batch(10)
    example_code = factories.CodeFactory.create()
    priority_queue_highest_priority_element = AnimationPriorityQueueElement(code=example_code, priority=10)
    priority_queue_highest_priority_element.save()
    
    returned_element = AnimationPriorityQueueElement.pop_first()

    assert AnimationPriorityQueueElement.objects.count() == 10
    assert returned_element.pk == priority_queue_highest_priority_element.pk

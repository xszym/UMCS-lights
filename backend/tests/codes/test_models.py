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


@pytest.mark.django_db
def test_config_model():
    config = Config(force_run = False, force_stop = False)
    config.save()

    assert Config.objects.count() == 1
    assert config.force_run == False
    

@pytest.mark.django_db
def test_config_model_save_multiple():
    try:
        factories.ConfigFactory.create_batch(3)
        assert False
    except:
        assert True


@pytest.mark.django_db
def test_priority_queue_model():
    example_code = factories.CodeFactory.create()
    p_queue = AnimationPriorityQueueElement(code=example_code, priority=10)
    p_queue.save()

    returned_element = AnimationPriorityQueueElement.objects.order_by('-priority').first()
    
    assert AnimationPriorityQueueElement.objects.count() == 1
    assert returned_element.priority == p_queue.priority


@pytest.mark.django_db
def test_priority_queue_model_mulitiple_objects():
    factories.AnimationPriorityQueueElementFactory.create_batch(10)
    
    assert AnimationPriorityQueueElement.objects.count() == 10


@pytest.mark.django_db
def test_priority_queue_model_return_higher_priority():
    example_code1 = factories.CodeFactory.create()
    example_code2 = factories.CodeFactory.create()
    p_queue_high_priority = factories.AnimationPriorityQueueElementFactory(code=example_code1, priority = 6)
    p_queue_high_priority.save()
    p_queue_low_priority = AnimationPriorityQueueElement(code=example_code2, priority = 3)
    p_queue_low_priority.save()
    
    returned_element = AnimationPriorityQueueElement.objects.order_by('-priority').first() 

    assert AnimationPriorityQueueElement.objects.count() == 2
    assert returned_element.pk == p_queue_high_priority.pk


@pytest.mark.django_db
def test_priority_queue_model_return_highest_priority():
    factories.AnimationPriorityQueueElementFactory.create_batch(10)
    example_code = factories.CodeFactory.create()
    p_queue_highest_priority = AnimationPriorityQueueElement(code=example_code, priority = 10)
    p_queue_highest_priority.save()
    
    returned_element = AnimationPriorityQueueElement.objects.order_by('-priority').first() 

    assert AnimationPriorityQueueElement.objects.count() == 11
    assert returned_element.pk == p_queue_highest_priority.pk

import factory
from codes.models import Code


class CodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Code

    name = factory.Sequence(lambda n: 'Project {}'.format(n))
    author = factory.Sequence(lambda n: 'Simon %s' % n)
    code = 'print(123)'
    is_example = False


class ConfigFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Config

    force_stop = False
    force_run = False
    

class AnimationPriorityQueueElementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AnimationPriorityQueueElement

    code = factory.SubFactory(CodeFactory)
    priority = 0
    
import factory
from codes.models import Code


class CodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Code

    name = factory.Sequence(lambda n: 'Project {}'.format(n))
    author = factory.Sequence(lambda n: 'Simon %s' % n)
    code = 'print(123)'
    is_example = False

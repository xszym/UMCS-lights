from codes.serializers import CodeSerializer


def test_valid_code_serializer():
    valid_serializer_data = {
        'name': 'TestCode',
        'author': 'maciej',
        'code': 'print("Hello World")',
        'description': 'example',
        'language': 0,
    }
    serializer = CodeSerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.data == valid_serializer_data
    assert serializer.errors == {}


def test_invalid_code_serializer():
    invalid_serializer_data = {
        'name': 'TestCode',
        'author': 'maciej',
        'code': '',
        'description': 'example',
        'language': 0,
    }
    serializer = CodeSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"code": ["This field may not be blank."]}

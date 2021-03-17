from rest_framework import serializers
from .models import Code


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ['pk', 'name', 'author', 'description', 'code', 'language']
        read_only_fields = ['pk']

from rest_framework import viewsets,permissions
from .serializers import CodeSerializer
from .models import Code


class CodeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post']
    serializer_class = CodeSerializer

    def get_queryset(self):
        queryset = Code.objects.filter(is_example=True)
        return queryset
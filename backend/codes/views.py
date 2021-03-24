from rest_framework import viewsets,permissions
from .serializers import CodeSerializer
from .models import Code


class AllCodesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post']
    serializer_class = CodeSerializer

    def get_queryset(self):
        queryset = Code.objects
        return queryset

class ExampleCodesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post']
    serializer_class = CodeSerializer

    def get_queryset(self):
        queryset = Code.objects.filter(is_example=True)
        return queryset

class NonExampleCodesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post']
    serializer_class = CodeSerializer

    def get_queryset(self):
        queryset = Code.objects.filter(is_example=False)
        return queryset

class ApprovedCodesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post']
    serializer_class = CodeSerializer

    def get_queryset(self):
        queryset = Code.objects.filter(approved=True)
        return queryset

class UnapprovedCodesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post']
    serializer_class = CodeSerializer

    def get_queryset(self):
        queryset = Code.objects.filter(approved=False)
        return queryset

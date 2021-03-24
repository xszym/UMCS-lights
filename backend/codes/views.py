from rest_framework import viewsets,permissions
from .serializers import CodeSerializer
from .models import Code


class CodesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post']
    serializer_class = CodeSerializer

    def get_queryset(self):

        queryset = Code.objects.all()
        example = self.request.query_params.get('example')
        approved = self.request.query_params.get('approved')
        if example:
            queryset = queryset.filter(is_example=example)
        elif approved:
            queryset = queryset.filter(approved=approved)
        return queryset

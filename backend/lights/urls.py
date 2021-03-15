from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from codes import views as codes_views
from .views import ping


router = routers.DefaultRouter()
router.register(r'code/?', codes_views.CodeViewSet, basename='Code')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ping/', ping, name='ping'),
    path('api/', include(router.urls))
]


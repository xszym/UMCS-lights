from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from codes import views as codes_views
from .views import ping, getDMXvalues, home


router = routers.DefaultRouter()
router.register(r'codes/?', codes_views.CodesViewSet, basename='codes')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('ping/', ping, name='ping'),
    path('DMXvalues', getDMXvalues, name='DMXvalues'),
    path('api/', include(router.urls))
]


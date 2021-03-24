from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from codes import views as codes_views
from .views import ping


router = routers.DefaultRouter()
router.register(r'codes/all', codes_views.AllCodesViewSet, basename='codes/all')
router.register(r'codes/approved', codes_views.ApprovedCodesViewSet, basename='codes/approved')
router.register(r'codes/unapproved', codes_views.UnapprovedCodesViewSet, basename='codes/unapproved')
router.register(r'codes/example', codes_views.ExampleCodesViewSet, basename='codes/example')
router.register(r'codes/nonexample', codes_views.NonExampleCodesViewSet, basename='codes/nonexample')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ping/', ping, name='ping'),
    path('api/', include(router.urls))
]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'business', BusinessViewSet)
router.register(r'revenue', RevenueViewSet)

app_name = 'business'

urlpatterns = [
    path('', include(router.urls)),
]
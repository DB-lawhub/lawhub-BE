from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'vat', VatViewSet)
router.register(r'incometax', IncomeTaxViewSet)
router.register(r'corporatetax', CorporateTaxViewSet)
router.register(r'rental', RentalViewSet)

app_name = 'tax'

urlpatterns = [
    path('', include(router.urls)),
]
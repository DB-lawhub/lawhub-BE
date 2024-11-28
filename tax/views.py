from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *

# Create your views here.
class VatViewSet(viewsets.ModelViewSet):
    queryset = VAT.objects.all()
    serializer_class = VatSerializer

class IncomeTaxViewSet(viewsets.ModelViewSet):
    queryset = IncomeTax.objects.all()
    serializer_class = IncomeTaxSerializer

class CorporateTaxViewSet(viewsets.ModelViewSet):
    queryset = CorporateTax.objects.all()
    serializer_class = CorporateTaxSerializer

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
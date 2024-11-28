from rest_framework import serializers
from .models import *

class VatSerializer(serializers.ModelSerializer):
    class Meta:
        model = VAT
        fields = '__all__'

class IncomeTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeTax
        fields = '__all__'

class CorporateTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorporateTax
        fields = '__all__'

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = '__all__'
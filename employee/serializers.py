from rest_framework import serializers
from .models import *

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSalary
        fields = '__all__'

class EmployeeTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeTax
        fields = '__all__'
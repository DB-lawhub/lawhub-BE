from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from .models import *
from .serializers import *

# Create your views here.
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeSalaryViewSet(viewsets.ModelViewSet):
    queryset = EmployeeSalary.objects.all()
    serializer_class = EmployeeSalarySerializer

    # 해당 직원의 급여 내역 반환
    @action(detail=False, methods=['get'], url_path='all/(?P<employee_id>[^/.]+)')
    def get_employee_salaries(self, request, employee_id=None):
        employee = get_object_or_404(Employee, pk=employee_id)
        salaries = EmployeeSalary.objects.filter(employee_id=employee)
        serializer = self.get_serializer(salaries, many=True)
        return Response(serializer.data)

class EmployeeTaxViewSet(viewsets.ModelViewSet):
    queryset = EmployeeTax.objects.all()
    serializer_class = EmployeeTaxSerializer
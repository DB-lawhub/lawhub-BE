from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import *
from .serializers import *

# Create your views here.
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        business_id = self.request.query_params.get('business_id', None)
        if business_id is not None:
            return Employee.objects.filter(business_id=business_id)
        return Employee.objects.none()
    
    def retrieve(self, request, *args, **kwargs):
        employee_id = kwargs.get('pk')

        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return Response({'detail': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

        # 직원을 찾으면 serializer로 반환
        serializer = self.get_serializer(employee)
        return Response(serializer.data)

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
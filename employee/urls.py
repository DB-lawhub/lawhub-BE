from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'employee', EmployeeViewSet)
router.register(r'employee-salary', EmployeeSalaryViewSet)
router.register(r'employee-tax', EmployeeTaxViewSet)

app_name = 'employee'

urlpatterns = [
    path('', include(router.urls)),
]
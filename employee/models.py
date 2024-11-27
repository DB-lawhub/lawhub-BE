from django.db import models
from business.models import Business
from decimal import Decimal

# Create your models here.
# 직원
class Employee(models.Model):
    TAX_TYPE_CHOICES = [
        ('4대보험', '4대보험'),
        ('3.3%', '3.3%'),
    ]
    
    employee_id = models.AutoField(primary_key=True)
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='employee')
    name = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)     # 월급
    hourly = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)     # 시급
    working_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    tax_type = models.CharField(max_length=10, choices=TAX_TYPE_CHOICES)
    join_date = models.DateField()      # 입사 날짜
    severance_pay = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)

# 직원 급여
class EmployeeSalary(models.Model):
    salary_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salaries')    # 역참조 문제 때문에 related_name이 복수형
    employee_date = models.DateField()      # 일한 달
    pay = models.DecimalField(max_digits=15, decimal_places=2, blank=True)      # 급여
    pay_date = models.DateField(null=True, blank=True)      # 급여 지급일

    # 월급 자동 계산
    def save(self, *args, **kwargs):
        employee = self.employee_id

        if employee.salary > 0:
            self.pay = employee.salary
        else:
            self.pay = employee.hourly * employee.working_hours * 4

        super().save(*args, **kwargs)

        # 주휴수당, 추가수당 추가하기

        # EmployeeTax 테이블 자동 생성
        tax_type = employee.tax_type
        if tax_type == "4대보험":
            EmployeeTax.objects.create(
                salary_id = self,
                employee_id = self.employee_id
            )

# 직원 세금
class EmployeeTax(models.Model):
    tax_id = models.AutoField(primary_key=True)
    salary_id = models.ForeignKey(EmployeeSalary, on_delete=models.CASCADE, related_name='tax')
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tax')
    employment = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)            # 고용보험
    industrial_accident = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)   # 산재보험
    health = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)                # 건강보험
    pension = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)               # 국민연금
    care = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)                  # 장기요양보험
    sum = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    payment_date = models.DateField(null=True, blank=True)

    # 4대보험 자동 계산
    def save(self, *args, **kwargs):
        employee_salary = self.salary_id
        salary = employee_salary.pay

        if self.employee_id.tax_type == '4대보험':
            self.employment = salary * Decimal(0.0115)
            self.industrial_accident = salary * Decimal(0.0105)  # !!! 업종별 상이한 산재보험료율
            self.health = salary * Decimal(0.03545)
            self.pension = salary * Decimal(0.045)
            self.care = self.health * 2 * Decimal(0.06475)
            self.sum = self.employment + self.industrial_accident + self.health + self.pension + self.care

        super().save(*args, **kwargs)
from django.db import models
from business.models import Business
from decimal import Decimal

# Create your models here.
# 부가가치세
class VAT(models.Model):
    LEVIER_TYPE_CHOICES = [
        ('일반과세자', '일반과세자'),
        ('간이과세자', '간이과세자'),
    ]
    
    vat_id = models.AutoField(primary_key=True)
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='vat')
    levier_type = models.CharField(max_length=10, choices=LEVIER_TYPE_CHOICES)
    sales_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    purchase_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    vat_tax = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    payment_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.levier_type == '일반과세자':
            self.vat_tax = self.sales_amount * Decimal(0.1) - self.purchase_amount * Decimal(0.1) - self.sales_amount * Decimal(0.013)
        else:
            business = self.business_id
            business_type = business.business_type
            # 간이과세자 업종별 부가가치율
            if business_type in [3, 25]:
                rate = 0.15
            elif business_type in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 19, 20, 21]:
                rate = 0.2
            elif business_type in [15, 16, 17, 18]:
                rate = 0.3
            elif business_type in [22, 26, 28]:
                rate = 0.4
            else:
                rate = 0.3
            
            self.vat_tax = self.sales_amount * Decimal(rate) * Decimal(0.1) - self.purchase_amount * Decimal(0.005)
            
        super().save(*args, **kwargs)


# 소득세
class IncomeTax(models.Model):
    income_id = models.AutoField(primary_key=True)
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='income_tax')
    total_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    expense_account = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    personal_allowance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pension_premium = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    tax_base = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=6, blank=True)
    progressive_deduction = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    children_deduction = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    income_tax = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    payment_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # 과세표준 계산
        self.tax_base = self.total_income - self.expense_account - self.personal_allowance - self.pension_premium
        
        # 세율 및 누진공제 계산
        if self.tax_base <= Decimal(14000000):
            self.tax_rate = Decimal(0.06)
        elif self.tax_base <= Decimal(50000000):
            self.tax_rate = Decimal(0.15)
            self.progressive_deduction = Decimal(1260000)
        elif self.tax_base <= Decimal(88000000):
            self.tax_rate = Decimal(0.24)
            self.progressive_deduction = Decimal(5760000)
        elif self.tax_base <= Decimal(150000000):
            self.tax_rate = Decimal(0.35)
            self.progressive_deduction = Decimal(15440000)
        elif self.tax_base <= Decimal(300000000):
            self.tax_rate = Decimal(0.38)
            self.progressive_deduction = Decimal(19940000)
        elif self.tax_base <= Decimal(500000000):
            self.tax_rate = Decimal(0.40)
            self.progressive_deduction = Decimal(25940000)
        elif self.tax_base <= Decimal(1000000000):
            self.tax_rate = Decimal(0.42)
            self.progressive_deduction = Decimal(35940000)
        else:
            self.tax_rate = Decimal(0.45)
            self.progressive_deduction = Decimal(65940000)

        self.income_tax = self.tax_base * self.tax_rate - self.progressive_deduction - self.children_deduction

        super().save(*args, **kwargs)

# 법인세
class CorporateTax(models.Model):
    corporate_id = models.AutoField(primary_key=True)
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='corporate_tax')
    corporate_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=9, blank=True)
    progressive_deduction = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    corporate_tax = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    payment_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # 세율 및 누진공제 계산
        if self.corporate_income < Decimal(200000000):
            self.tax_rate = Decimal(0.09)
        elif self.corporate_income < Decimal(20000000000):
            self.tax_rate = Decimal(0.19)
            self.progressive_deduction = Decimal(20000000)
        elif self.corporate_income < Decimal(300000000000):
            self.tax_rate = Decimal(0.21)
            self.progressive_deduction = Decimal(420000000)
        else:
            self.tax_rate = Decimal(0.24)
            self.progressive_deduction = Decimal(9420000000)

        self.corporate_tax = self.corporate_income * self.tax_rate - self.progressive_deduction

        super().save(*args, **kwargs)

# 임대료
class Rental(models.Model):
    lease_id = models.AutoField(primary_key=True)
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='rental')
    deposit = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    rent = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    payment_date = models.DateField(null=True, blank=True)
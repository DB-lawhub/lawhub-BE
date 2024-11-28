from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 사업
class Business(models.Model):
    BUSINESS_REGISTRATION_CHOICES = [
        ('개인', '개인'),
        ('법인', '법인'),
    ]

    business_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business')
    business_registration = models.CharField(max_length=10, choices=BUSINESS_REGISTRATION_CHOICES, default='개인')
    number_of_employees = models.PositiveIntegerField(default=0, blank=True)
    business_type = models.IntegerField()

# 사업 수익
class Revenue(models.Model):
    revenue_id = models.AutoField(primary_key=True)
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='revenue')
    revenue_data = models.DateField()
    revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0)
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(VAT)
admin.site.register(IncomeTax)
admin.site.register(CorporateTax)
admin.site.register(Rental)
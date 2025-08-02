from django.contrib import admin

# Register your models here.
from .models import Customer, CustomerStatement

admin.site.register(Customer)
admin.site.register(CustomerStatement)
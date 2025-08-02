from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    # Default opening balance to 0.0 if not provided
    # This ensures that the field is always initialized
    opening_balance = models.FloatField(default=0)

    def __str__(self):
        return self.name

class CustomerStatement(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()
    credit = models.FloatField(default=0)
    debit = models.FloatField(default=0)
    balance = models.FloatField()

    def __str__(self):
        return f"{self.customer.name} - {self.date} - {self.description}"

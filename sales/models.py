from django.db import models
from customer.models import Customer

class Sale(models.Model):
    PAYMENT_CHOICES = [
        ("Cash", "Cash"),
        ("Credit", "Credit"),
        ("UPI", "UPI"),
        ("Bank", "Bank"),
    ]

    UNIT_CHOICES = [("Brass", "Brass"),("Ton", "Ton"), ("Cubic Meter", "Cubic Meter")]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    qty = models.FloatField()
    rate = models.FloatField()
    amount = models.FloatField()
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    date = models.DateField()

    def __str__(self):
        return f"{self.customer.name} - {self.material} - {self.date}"

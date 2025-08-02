from django.db import models

class Sale(models.Model):
    PAYMENT_CHOICES = [
        ("Cash", "Cash"),
        ("Credit", "Credit"),
        ("UPI", "UPI"),
        ("Bank", "Bank"),
    ]

    customer = models.CharField(max_length=100)
    vehicle = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    qty = models.FloatField()
    rate = models.FloatField()
    amount = models.FloatField()
    unit = models.CharField(max_length=20)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    date = models.DateField()

    def __str__(self):
        return f"{self.customer} - {self.material} - {self.date}"

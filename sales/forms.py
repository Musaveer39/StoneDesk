# forms.py
from django import forms
from .models import Sale, Customer

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer', 'vehicle', 'material', 'qty', 'rate', 'amount', 'unit', 'payment_mode', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

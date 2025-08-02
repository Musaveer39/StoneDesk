from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, CustomerStatement
from django.db import IntegrityError
from django.utils import timezone

def customer_dashboard(request):
    customers = Customer.objects.all()

    customer_data = []
    for customer in customers:
        last_entry = CustomerStatement.objects.filter(customer=customer).order_by('-date', '-id').first()
        balance = last_entry.balance if last_entry else customer.opening_balance
        customer_data.append({
            'customer': customer,
            'balance': balance
        })

    return render(request, 'customer_dashboard.html', {
        'customer_data': customer_data
    })


def add_customer(request):
    error_message = ''
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        contact = request.POST.get('contact', '').strip()
        address = request.POST.get('address', '').strip()
        opening_balance_raw = request.POST.get('opening_balance', '0').strip()

        # Convert opening_balance to float safely
        try:
            opening_balance = float(opening_balance_raw) if opening_balance_raw else 0.0
        except ValueError:
            opening_balance = 0.0
            error_message = "Invalid opening balance provided. Defaulted to 0."

        if name:
            if Customer.objects.filter(name=name).exists():
                error_message = f"A customer named '{name}' already exists!"
            else:
                try:
                    Customer.objects.create(
                        name=name,
                        contact=contact,
                        address=address,
                        opening_balance=opening_balance
                    )
                    return redirect('customer_dashboard')
                except IntegrityError:
                    error_message = "Something went wrong while saving. Try again."
        else:
            error_message = "Customer name is required."

    return render(request, 'add_customer.html', {'error_message': error_message})



def customer_statement(request, customer_id):
    selected_customer = get_object_or_404(Customer, id=customer_id)
    statements = CustomerStatement.objects.filter(customer=selected_customer).order_by('date')
    print("Customer Statement:", statements)  # Debugging line to check fetched statements
    return render(request, 'customer_statement.html', {
        'selected_customer': selected_customer,
        'statements': statements,
    })

def pay_due(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        last_entry = CustomerStatement.objects.filter(customer=customer).order_by('-date', '-id').first()
        prev_balance = last_entry.balance if last_entry else customer.opening_balance
        new_balance = prev_balance - amount

        CustomerStatement.objects.create(
            customer=customer,
            date=timezone.now().date(),
            description="Payment Received",
            credit=0,
            debit=amount,
            balance=new_balance
        )

        return redirect('customer_dashboard')

    return render(request, 'pay_due.html', {'customer': customer})
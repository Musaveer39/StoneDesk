from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from .models import Sale
from .forms import SaleForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from customer.models import Customer, CustomerStatement


def sales_dashboard(request):
    today = timezone.now().date()
    filter_option = request.GET.get('filter', 'today')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Determine the date range based on the filter option
    if filter_option == 'this_week':
        start = today - timedelta(days=today.weekday())  # Monday of this week
        end = today
    elif filter_option == 'this_month':
        start = today.replace(day=1)
        end = today
    elif filter_option == 'custom' and start_date and end_date:
        try:
            start = timezone.datetime.strptime(start_date, "%Y-%m-%d").date()
            end = timezone.datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            start = end = today  # Fallback to today if parsing fails
    else:  # Default: today
        start = end = today

    sales = Sale.objects.filter(date__range=(start, end)).order_by('-date')
    total_amount = sales.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'sales': sales,
        'total_amount': total_amount,
        'start': start,
        'end': end,
        'filter_option': filter_option,
        'today': today,
    }
    return render(request, 'sales_dashboard.html', context)




# views.py
from .forms import SaleForm

def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.amount = sale.qty * sale.rate  # calculate amount
            sale.save()

            # If credit, update customer statement
            if sale.payment_mode == "Credit":
                last_entry = CustomerStatement.objects.filter(customer=sale.customer).order_by('-date', '-id').first()
                previous_balance = last_entry.balance if last_entry else sale.customer.opening_balance
                new_balance = previous_balance + sale.amount

                CustomerStatement.objects.create(
                    customer=sale.customer,
                    date=sale.date,
                    description=f"Credit Sale - {sale.material} (Qty: {sale.qty} {sale.unit})",
                    credit=sale.amount,
                    debit=0,
                    balance=new_balance
                )

            return redirect('sales_dashboard')
    else:
        form = SaleForm()

    return render(request, 'create_sale.html', {'form': form})


def sale_update(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    old_amount = sale.amount
    old_payment_mode = sale.payment_mode
    old_date = sale.date

    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            updated_sale = form.save(commit=False)
            updated_sale.amount = updated_sale.qty * updated_sale.rate
            updated_sale.save()

            # Handle CustomerStatement adjustment if payment mode is credit
            if old_payment_mode == 'Credit':
                # Delete the old statement
                CustomerStatement.objects.filter(
                    customer=sale.customer,
                    date=old_date,
                    credit=old_amount,
                    description__icontains="Credit Sale"
                ).delete()

            if updated_sale.payment_mode == "Credit":
                # Recalculate balance
                last_entry = CustomerStatement.objects.filter(
                    customer=updated_sale.customer
                ).order_by('-date', '-id').first()

                previous_balance = last_entry.balance if last_entry else updated_sale.customer.opening_balance
                new_balance = previous_balance + updated_sale.amount

                CustomerStatement.objects.create(
                    customer=updated_sale.customer,
                    date=updated_sale.date,
                    description=f"Credit Sale - {updated_sale.material} (Qty: {updated_sale.qty} {updated_sale.unit})",
                    credit=updated_sale.amount,
                    debit=0,
                    balance=new_balance
                )

            return redirect('sales_dashboard')
    else:
        form = SaleForm(instance=sale)

    return render(request, 'create_sale.html', {'form': form})

def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        return redirect('sales_dashboard')
    return render(request, 'sale_confirm_delete.html', {'sale': sale})

def print_invoice(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'print.html', {'sale': sale})

def print_dc(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'print_dc.html', {'sale': sale})

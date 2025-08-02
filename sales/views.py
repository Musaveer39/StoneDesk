from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from .models import Sale
from .forms import SaleForm
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

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


def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_dashboard')
    else:
        form = SaleForm()
    return render(request, 'sale_form.html', {'form': form})

def sale_update(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    form = SaleForm(request.POST or None, instance=sale)
    if form.is_valid():
        form.save()
        return redirect('sales_dashboard')
    return render(request, 'sale_form.html', {'form': form})

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

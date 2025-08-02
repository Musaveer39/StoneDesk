from django.shortcuts import render, redirect, get_object_or_404
from .models import Sale
from .forms import SaleForm
from django.utils.timezone import now
from django.db.models import Sum
from datetime import date

def sale_list(request):
    sales = Sale.objects.all().order_by('-date')
    return render(request, 'sales/sale_list.html', {'sales': sales})

def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sale_list')
    else:
        form = SaleForm()
    return render(request, 'sales/sale_form.html', {'form': form})

def sale_update(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    form = SaleForm(request.POST or None, instance=sale)
    if form.is_valid():
        form.save()
        return redirect('sale_list')
    return render(request, 'sales/sale_form.html', {'form': form})

def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        return redirect('sale_list')
    return render(request, 'sales/sale_confirm_delete.html', {'sale': sale})

def todays_sales_total(request):
    today = date.today()
    total = Sale.objects.filter(date=today).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    return render(request, 'sales/todays_sales.html', {'total': total})

def sales_dashboard(request):
    today = timezone.now().date()
    sales = Sale.objects.filter(date=today)
    
    total_amount = sum(s.amount for s in sales)

    return render(request, 'sales_dashboard.html', {
        'sales': sales,
        'total_amount': total_amount,
        'today': today
    })
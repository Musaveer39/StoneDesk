"""
URL configuration for StoneDesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import login_view, dashboard
from sales.views import sales_dashboard, sale_create, sale_update, sale_delete, print_invoice, print_dc
from customer.views import customer_dashboard, add_customer, customer_statement,pay_due

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),  # Login view
    path('dashboard/', dashboard, name='dashboard'),  # Dashboard view
    path('sales/', sales_dashboard, name='sales_dashboard'),
    
    path('add/', sale_create, name='sale_create'),
    path('edit/<int:pk>/', sale_update, name='sale_edit'),
    path('delete/<int:pk>/', sale_delete, name='sale_delete'),
    path('print/<int:pk>/', print_invoice, name='print_invoice'), 
    path('print_dc/<int:pk>/', print_dc, name='print_dc'),  # Print delivery challan view
    path('customers/', customer_dashboard, name='customer_dashboard'),
    path('customers/add/', add_customer, name='add_customer'),
    path('customers/statement/<int:customer_id>/', customer_statement, name='customer_statement'),
    path('customers/pay_due/<int:customer_id>/', pay_due, name='pay_due'),  # Pay due view
    
]

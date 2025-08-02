from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')  # Redirect based on role if needed
        messages.error(request, "Invalid credentials")
    return render(request, 'login.html')


def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})
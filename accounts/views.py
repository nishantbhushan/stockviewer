from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Create your views here.
def login_view(request):
    context={}
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/portfolio/')
    else:
        form = AuthenticationForm(request)
    context['form'] = form
    return render(request, 'login.html', context)

def logout_view(request):
    context={}
    if request.method == "POST":
        logout(request)
        return redirect('/accounts/login')
    return render(request, 'logout.html', context)

def register_view(request):
    context={}
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect ('login')
    context['form'] = form
    return render(request, 'register.html', context)
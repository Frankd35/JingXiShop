from django.shortcuts import render


# Create your views here.


def reg_view(request):
    return render(request, 'register.html')


def login_view(request):
    return render(request, 'login.html')


def logout_view(request):
    return None

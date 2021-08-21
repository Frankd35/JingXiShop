from django.shortcuts import render


# Create your views here.


def reg_view(request):
    return render(request, 'register.html')


def login_view(request):
    return render(request, 'login.html')


def logout_view(request):
    return None


def usr_info_view(request):
    user = {}
    return render(request,'user_center_info.html',user)


def usr_site_view(request):
    address = {}
    return render(request,'user_center_site.html',address)

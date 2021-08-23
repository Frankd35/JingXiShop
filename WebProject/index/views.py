from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from user.models import User


def index_view(request):
    return render(request, 'index.html')


def index_template_view(request):
    usr_id = int(request.session.get('uid', -1))
    isLogin = usr_id != -1
    if not isLogin:
        render(request, 'index_template.html', {'isLogin': isLogin})
    user = User.objects.get(id=usr_id)
    return render(request, 'index_template.html', {'isLogin': isLogin, 'user': user})

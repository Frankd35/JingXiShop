from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
# from sympy.codegen.ast import none

from user.models import User
from goods.models import Category, Comment
from goods.models import Goods


def index_view(request):
    return render(request, 'index.html')


def index_template_view(request):
    usr_id = int(request.session.get('uid', -1))
    isLogin = usr_id != -1

    if not isLogin:
        render(request, 'index_template.html', {'isLogin': isLogin})
        # HttpResponseRedirect('index_template')
    try:
        user = User.objects.get(id=usr_id)
    except:
        user = None
    GoodsCategoryList = Category.objects.filter(state=1)[0:6]
    hotgoodsList = Goods.objects.filter(id=1).order_by('searching_num')

    return render(request, 'index_template.html',
                  {'isLogin': isLogin, 'user': user, 'GoodsCategoryList': GoodsCategoryList,
                   'hotgoodsList': hotgoodsList})

from itertools import chain
from typing import List, Any

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
    # 商品分类图
    GoodsCategoryList = Category.objects.filter(state=1)[0:6]
    # 热点图
    hotgoodsList = Goods.objects.filter(category_id=1).order_by('searching_num')[0:2]
    # 轮播图
    slideList = Goods.objects.filter(category_id=0).order_by('-searching_num')
    tmp: List[Any] = []
    for category in GoodsCategoryList:
        GoodsList = Goods.objects.filter(category_id__gte=category.id).order_by('category_id')
        tmp = [tmp, GoodsList]
    tmp = chain(tmp)
    return render(request, 'index_template.html',
                  {'isLogin': isLogin, 'user': user, 'GoodsCategoryList': GoodsCategoryList,
                   'hotgoodsList': hotgoodsList, 'slideList': slideList, 'tmp': tmp})

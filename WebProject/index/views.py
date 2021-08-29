from itertools import chain
from typing import List, Any

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
# from sympy.codegen.ast import none
from user.models import User, Shop
from goods.models import Category, Comment, Goods


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
    hotgoodsList = Goods.objects.filter(category_id=2000).order_by('searching_num')[0:2]
    # 轮播图
    slideList = Goods.objects.filter(category_id=0).order_by('-searching_num')
    # tmp: List[Any] = []
    # for category in GoodsCategoryList:
    #     GoodsList = Goods.objects.filter(category_id__gte=category.id).order_by('category_id')
    #     tmp = [tmp, GoodsList]
    # tmp = chain(tmp)
    # 新品推荐
    newGoodsList = Goods.objects.all()
    if len(newGoodsList) > 5:
        newGoodsList = newGoodsList[len(newGoodsList) - 6: len(newGoodsList) - 1]
    print(newGoodsList)
    # 商品
    GoodsList=[];
    # GoodsList1 = Goods.objects.filter(category_id__gte=1, searching_num__lte=99999).order_by('category_id')
    # 介绍
    bannerList = Goods.objects.filter(category_id__gte=11)
    for i in range(1,8,1):
        GoodsList[i*5-5:i*5] = Goods.objects.filter(category_id=i).order_by('category_id')[0:5]


    return render(request, 'index_template.html',
                  {'isLogin': isLogin, 'user': user, 'GoodsCategoryList': GoodsCategoryList,
                   'hotgoodsList': hotgoodsList, 'slideList': slideList, 'GoodsList': GoodsList,
                   'bannerList': bannerList, 'newGoodsList': newGoodsList})


def list_template_view(request):
    # 获取cookies里的当前登录用户id
    usr_id = int(request.session.get('uid', -1))
    isLogin = usr_id != -1
    try:
        user = User.objects.get(id=usr_id)
    except Exception as e:
        user = None
    # 判断请求方式
    kw = request.GET.get('keyword')
    category_id = request.GET.get('category')
    goodsList = None
    currentCategory = None
    # 新品推荐
    newGoodsList = Goods.objects.all()
    if len(newGoodsList) > 5:
        newGoodsList = newGoodsList[len(newGoodsList) - 6: len(newGoodsList) - 1]

    # 支持精确查询商品、店铺、类别
    if kw:
        kw = kw.split()
        goodsList = Goods.objects.filter(name__contains=kw[0])
        # 找出关联度最高的
        for i in kw:
            goodsList = goodsList.filter(name__icontains=i)
        for gname in kw:
            _by_name = Goods.objects.filter(name__icontains=gname)
            goodsList = goodsList | _by_name
        for sname in kw:
            _ = Shop.objects.filter(name__contains=sname)
            for shop in _:
                _by_shop = Goods.objects.filter(shop_id=shop.id)
                goodsList = goodsList | _by_shop
        for cname in kw:
            _ = Category.objects.filter(name__contains=cname)
            for category in _:
                _by_category = Goods.objects.filter(category_id=category.id)
                goodsList = goodsList | _by_category
        goodsList.distinct()
    elif category_id:
        goodsList = Goods.objects.filter(category_id=int(category_id))
        currentCategory = Category.objects.filter(id=int(category_id)).first()
    goodsList_price = None if not goodsList \
        else sorted(goodsList, key=lambda x: x.price)
    goodsList_hot = None if not goodsList \
        else sorted(goodsList, key=lambda x: x.searching_num)
    GoodsCategory = Category.objects.all()
    return render(request, "list_template.html",
                  {'isLogin': isLogin, 'user': user, 'goodsList': goodsList, 'goodsList_hot': goodsList_hot,
                   'goodsList_price': goodsList_price, 'GoodsCategory': GoodsCategory,
                   'currentCategory': currentCategory, 'newGoodsList': newGoodsList})

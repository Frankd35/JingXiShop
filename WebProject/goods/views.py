import json
import random
from django.shortcuts import render
from user import models as user_model
from goods.models import Goods
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .detail_response import *


class TempUser:
    def __init__(self, id, name, img, isLogin, addr_id, is_merchant):
        self.id = id
        self.name = name
        self.img = img
        self.isLogin = isLogin
        self.addr_id = addr_id
        self.is_merchant = is_merchant


def getLoginState(request):
    is_merchant = 0
    isLogin = False
    user_id = -1
    user_name = ""
    user_img = ""
    user_addr_id = -1
    # 判断是否登录, 并从session获取登录状态
    if request.session.get('username') and request.session.get('uid'):
        isLogin = True
        user_name = request.session.get('username')
        user_id = request.session.get('uid')
        user_img = request.session.get('userimg')
        tempUser = user_model.User.objects.filter(id=user_id).first()
        user_addr_id = tempUser.addr_id
        is_merchant = tempUser.is_merchant
    return TempUser(user_id, user_name, user_img, isLogin, user_addr_id, is_merchant)


# Create your views here.
def detail_view(request):
    user = getLoginState(request)
    m = request.method
    # GET请求， 加载页面
    if m == 'GET':
        goods_id = int(request.GET.get('gid', ''))
        print("GET method ,gid=%d" % goods_id)
        good = getGoodsDetail(goods_id)
        shop = getShopDetail(good.shop_id)
        commentList = getCommentList(goods_id)
        category = getCategory(good.category_id)
        cateList = getCateList()
        # 猜你喜欢
        newGoodsList = Goods.objects.filter(category_id=good.category_id)
        randomGoods = newGoodsList[random.randint(0,len(newGoodsList)-1)]
        newGoodsList = sorted(newGoodsList, key=lambda x: x.searching_num, reverse=True)
        newGoodsList = newGoodsList[:10]
        random.shuffle(newGoodsList)
        newGoodsList = newGoodsList[:3]
        newGoodsList.append(randomGoods)
        return render(request, 'detail_template.html',
                      {'user': user, 'isLogin': user.isLogin, 'good': good, 'shop': shop, 'commentList': commentList,
                       'category': category, 'GoodsCategoryList': cateList,
                       'newGoodsList': newGoodsList})
    else:
        if user.id == -1:
            return HttpResponseRedirect('/login')
        # 判断是否是ajax发送来的POST请求
        num = int(request.POST.get('num', -1))
        gid = int(request.POST.get('gid', -1))
        print("POST method, gid=%d, num=%d" % (gid, num))
        if request.POST.getlist('buynow'):
            if (num >= 0) and (gid >= 0):
                errMsg = buyNow(user.id, gid, num)
                if errMsg != "":
                    return HttpResponse(errMsg)
            return HttpResponseRedirect('/order')
        elif request.POST.getlist('addcart'):
            if (num >= 0) and (gid >= 0):
                errMsg = addCart(user.id, gid, num)
                if errMsg != "":
                    return HttpResponse(errMsg)
            return HttpResponseRedirect('/cart')
        elif request.POST.getlist('addcollect'):
            addCollect(user.id, gid)
            return HttpResponseRedirect('/favorite')
        data = request.body.decode("utf-8")
        json_data = json.loads(data)
        print(json_data)
        gid = int(json_data.get('gid', -1))
        flag = str(json_data.get('flag', ''))
        text = str(json_data.get('text', ''))
        mark = float(json_data.get('mark', 1.0))
        if flag == 'editComment':  # ajax发送的POST请求
            print("新增评论")
            res = editComment(user.id, gid, text, mark)
            return JsonResponse({'res': res})
        print("并没有取到POST的表单")
        return HttpResponse("没有取到POST表单")

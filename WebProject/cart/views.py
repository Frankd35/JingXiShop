import json

from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from user import models as user_model
from django.shortcuts import render
from .cart_response import *
from .collect_response import *
from .orderplace_response import *
from .orderlist_response import *


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


# Cart  ->  view
def cart_view(request):
    user = getLoginState(request)
    m = request.method
    # GET请求， 加载页面
    if user.id == -1:
        return HttpResponseRedirect('/login')
    if m == 'GET':
        goodsList = dealRequest(user.id, 0, 0, 0)
        if len(goodsList) != 0:
            total_price = goodsList[len(goodsList) - 1].tttprice
        else:
            total_price = 0
        return render(request, 'shopcar2.html', {'goodsList': goodsList, 'user': user, 'total_price': total_price})
    # POST请求， 根据请求中flag的值判断操作类型
    else:
        data = request.body.decode("utf-8")
        json_data = json.loads(data)
        print(json_data)
        gid = int(json_data.get('gid', -1))
        flag = json_data.get('flag', '')
        isChosen = int(json_data.get('checked', 0))
        num = int(json_data.get('num', -1))
        goodsList = []
        total_price = 0
        if flag == 'check':  # check逻辑
            dealRequest(user.id, 1, gid, isChosen)
        elif flag == 'plus':  # add 逻辑
            dealRequest(user.id, 2, gid, 0)
        elif flag == 'sub':  # sub 逻辑
            dealRequest(user.id, 3, gid, 0)
        elif flag == 'delete':  # delete 逻辑
            dealRequest(user.id, 4, gid, 0)
        elif flag == 'allSellect':  # 全选 or 全不选
            dealRequest(user.id, 5, gid, isChosen)
        elif flag == 'updatenum': # 更新购物车商品数量
            dealRequest(user.id, 6, gid, num)
        return JsonResponse({"res": 1})


# Orderplace -> view
def orderplace_view(request):
    addr = []
    goodsList = []
    total_price = 0
    count = 0
    realPay = 0
    user = getLoginState(request)
    if user.id == -1:
        return HttpResponseRedirect('/login')
    m = request.method
    # GET请求， 加载页面
    if m == 'GET':
        if user.isLogin == False:
            return HttpResponseRedirect('/index_template')
        goodsList = OrderPlaceRequest(user.id)
        count = len(goodsList)
        addr = GetAddr(user.id)
        if len(goodsList) != 0:
            total_price = goodsList[len(goodsList) - 1].tttprice
        else:
            total_price = 0
        realPay = total_price + (count * 10)
        return render(request, 'place_order2.html',
                      {'goodsList': goodsList, 'addr': addr, 'total_price': total_price, 'user': user, 'count': count,
                       'realPay': realPay})
    else:
        flag = str(request.POST.get('settleorder', ''))
        if flag == 'ok':
            print("结算，提交订单")
            settleOrder(user.id, user.addr_id)
            return HttpResponseRedirect('/user_center_order')
        else:
            print("更改默认地址")
            data = request.body.decode("utf-8")
            json_data = json.loads(data)
            print(json_data)
            addr_id = int(json_data.get('address', -1))
            setDefaultAddr(user.id, addr_id)
            return JsonResponse({"res": 1})


# Collect  ->  view
def collect_view(request):
    user = getLoginState(request)
    if user.id == -1:
        return HttpResponseRedirect('/login')
    m = request.method
    # GET请求， 加载页面
    goodsList = []
    if m == 'GET':
        goodsList = collectRequest(user.id)
        return render(request, "collect2.html", {'goodsList': goodsList, 'user':user})
    else:
        print("删除收藏商品")
        data = request.body.decode("utf-8")
        json_data = json.loads(data)
        print(json_data)
        goods_id = int(json_data.get('goods_id', -1))
        deleteCollect(user.id, goods_id)
        return JsonResponse({"res": 1})




# Orderlist -> view
def orderlist_view(request):
    user = getLoginState(request)
    if user.id == -1:
        return HttpResponseRedirect('/login')
    m = request.method
    # GET请求， 加载页面
    if m == 'GET':
        orderList = getOrderList(user.id)
        return render(request, 'orderlist2.html', {'orderList': orderList, 'user': user})
    else:  # 接受ajax请求，确认收货
        print("响应POST请求")
        data = request.body.decode("utf-8")
        json_data = json.loads(data)
        print(json_data)
        oid = int(json_data.get('oid', -1))
        confirmOrder(oid)
        return JsonResponse({"res": 1})

import json

from django.shortcuts import render

from django.shortcuts import render
from .cart_response import *
from .collect_response import *
from .orderplace_response import *


class TempUser:
    def __init__(self, id, name, img, isLogin):
        self.id = id
        self.name = name
        self.img = img
        self.isLogin = isLogin


# Create your views here.
def cart_view(request):
    isLogin = False
    user_id = -1
    user_name = ""
    user_img = ""
    gid = 0
    # 判断是否登录, 并从session获取登录状态
    if request.session.get('username') and request.session.get('uid'):
        isLogin = True
        user_name = request.session.get('username')
        user_id = request.session.get('uid')
        user_img = request.session.get('userimg')
    user = TempUser(user_id, user_name, user_img, isLogin)

    m = request.method
    # GET请求， 加载页面
    if m == 'GET':
        goodsList = dealRequest(user_id, 0, gid, 0)
        if len(goodsList) != 0:
            total_price = goodsList[len(goodsList) - 1].tttprice
        else:
            total_price = 0
        print('Total_price:'+str(total_price))
        return render(request, 'shopcar2.html', {'goodsList': goodsList, 'user': user, 'total_price': total_price})
    # POST请求， 根据请求中flag的值判断操作类型
    else:
        data = request.body.decode("utf-8")
        json_data = json.load(data)
        gid = int(json_data.get('gid', -1))
        flag = json_data.get('flag', '')
        isChosen = bool(json_data.get('checked', False))
        goodsList = []
        total_price = 0
        if flag == 'check':  # check逻辑
            goodsList = dealRequest(user_id, 1, gid, isChosen)
        elif flag == 'plus':  # add 逻辑
            goodsList = dealRequest(user_id, 2, gid, 0)
        elif flag == 'sub':  # sub 逻辑
            goodsList = dealRequest(user_id, 3, gid, 0)
        elif flag == 'delete':  # delete 逻辑
            goodsList = dealRequest(user_id, 4, gid, 0)
        if len(goodsList) != 0:
            total_price = goodsList[len(goodsList) - 1].tttprice
        else:
            total_price = 0
        return render(request, 'shopcar2.html', {'goodsList': goodsList, 'user': user, 'total_price':total_price})


def collect_view(request):
    return None


def orderplace_view(request):
    return None

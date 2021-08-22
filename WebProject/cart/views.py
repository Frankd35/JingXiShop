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
        goodsList = dealRequest(user_id)
        return render(request, 'shopcar2.html', {'goodsList': goodsList, 'user': user})
    # POST请求， 根据请求中flag的值判断操作类型
    else:
        flag = request.POST.get('flag', '')
        if flag == 'check':  # check逻辑
            a = 1
        elif flag == 'add':  # add 逻辑
            b = 1
        elif flag == 'sub':  # sub 逻辑
            c = 1
        elif flag == 'delete':  # delete 逻辑
            d = 1

        return HttpResponse("加载失败")


def collect_view(request):
    return None


def orderplace_view(request):
    return None

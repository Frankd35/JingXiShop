from django.shortcuts import render

from django.shortcuts import render
from .cart_response import *
from .collect_response import *
from .orderplace_response import *


# Create your views here.
def cart_view(request):
    m = request.method
    user_id = 2
    if m == 'GET':
        goodsList = dealRequest(user_id)
        return render(request, 'shopcar2.html', {'goodsList': goodsList})
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

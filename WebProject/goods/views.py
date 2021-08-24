from django.shortcuts import render
from user import models as user_model
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .detail_response import *

class TempUser:
    def __init__(self, id, name, img, isLogin, addr_id):
        self.id = id
        self.name = name
        self.img = img
        self.isLogin = isLogin
        self.addr_id = addr_id


def getLoginState(request):
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
        user_addr_id = user_model.User.objects.filter(id=user_id)[0].addr_id
    return TempUser(user_id, user_name, user_img, isLogin, user_addr_id)

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
        return render(request, 'detail_template.html', {'user': user, 'isLogin': user.isLogin, 'good': good, 'shop': shop, 'commentList': commentList})
    else:
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

        print("并没有取到POST的表单")
        return None
import hashlib
import json
import re
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

import cart.orderlist_response
from cart.models import Order
from goods.models import Goods
from .models import User, Address, Shop


# Create your views here.


def reg_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        # 获取必要的参数
        username = request.POST.get('user_name')
        password_1 = request.POST.get('pwd')
        password_2 = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        img = "/static/images/defaultUserImg.png"
        print(allow)
        # 进行数据判断，所有信息均填写-->密码是否一致--> 邮箱格式是否一致-->协议是否勾选
        if not all([username, password_1, password_2, email]):
            # 数据缺失，在register填写过程中也会体现
            return render(request, 'register.html', {'errmsg': '您填写的数据不全'})
        if password_1 != password_2:
            return render(request, 'register.html', {'errmsg': '您两次填写的密码不一致'})
            # return HttpResponse('两次密码输入不一致')
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '您填写的邮箱格式不正确'})
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请您先勾选同意协议'})
        # 检查用户名是否被注册
        # try:
        #     user = User.objects.get(username=username)
        # except User.DoesNotExist:
        #     user = None
        user_exist = len(User.objects.filter(name=username))
        if user_exist:
            return render(request, 'register.html', {'errmsg': '您的用户名已经被注册，请重新注册'})
            # return HttpResponse('用户名已经注册')

        #   准备开始存储用户的信息到数据库

        # 哈希算法 给定明文，计算出一段定长的，不可逆的值 md5
        # 特点
        # 1.定长输出 MD5 32位16进制
        # 2.不可逆，无法反向计算出对应的明文
        # 3.雪崩效应
        m = hashlib.md5()
        m.update(password_1.encode())
        password_m = m.hexdigest()
        # 可能存在并发写入问题 捕获异常
        try:
            user = User.objects.create(name=username, pwd=password_m, email=email, img=img, is_merchant=0)
        except Exception as e:
            # 有可能报错，唯一索引注意并发写入问题
            print('--create user error %s' % e)
            return render(request, 'register.html', {'errmsg': '您的用户名已经被注册，请重新注册'})
        # request.session['username'] = username
        # request.session['uid'] = user.id
        return HttpResponseRedirect('/index_template')


def login_view(request):
    if request.method == 'GET':
        # 获取登录页面
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect('/index_template')
            # return HttpResponse('已登录')
        # 检查cookies
        c_username = request.COOKIES.get('username')
        c_uid = request.COOKIES.get('uid')
        checked = 'unchecked'
        if c_username and c_uid:
            # 回写session
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            checked = 'checked'
            return HttpResponseRedirect('/index_template')
            # return HttpResponse('已登录')

        return render(request, 'login.html', {'username': c_username, 'checked': checked})

    elif request.method == 'POST':
        # 处理数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})
        try:
            user = User.objects.get(name=username)
        except Exception as e:
            print('--login user error %s' % e)
            return render(request, 'register.html', {'errmsg': '您的用户名未进行注册'})
        # 比对密码
        m = hashlib.md5()
        m.update(password.encode())

        if m.hexdigest() != user.pwd:
            print("密码错误", m.hexdigest())
            return render(request, 'login.html', {'errmsg': '您的用户名和密码有错误'})
        # 记录会话状态
        request.session['username'] = username
        request.session['uid'] = user.id
        request.session['userimg'] = user.img
        resp = HttpResponseRedirect('/index_template')
        # 判断用户是否点选了 记住用户名
        # 点选了 --> Cookies 存储username uid 3天
        if 'remember' in request.POST:
            resp.set_cookie('username', username, 3600 * 24 * 3)
            resp.set_cookie('uid', user.id, 3600 * 24 * 3)
            resp.set_cookie('userimg', user.img, 3600 * 24 * 3)
        return resp

    # return render(request, 'login.html')


def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    # 删除COOKIES
    resp = HttpResponseRedirect('/index_template')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    return resp


def usr_info_view(request):
    # 获取cookies里的当前登录用户id
    usr_id = int(request.session.get('uid', -1))
    isLogin = usr_id != -1
    # 若用户未登录
    if not isLogin:
        return HttpResponseRedirect('login')  # not defined
    user = User.objects.get(id=usr_id)
    try:
        default_addr = Address.objects.get(id=user.addr_id)
    except Exception as e:
        print(e)
        default_addr = None
    return render(request, 'user_center_info2.html',
                  {'user': user, 'address': None, 'isLogin': isLogin, 'default_addr': default_addr})


def usr_site_view(request):
    # 获取cookies里的当前登录用户id
    usr_id = int(request.session.get('uid', -1))
    isLogin = usr_id != -1
    # 若用户未登录
    if not isLogin:
        return HttpResponseRedirect('login')  # not defined
    # 获取数据
    user = User.objects.get(id=usr_id)
    try:
        default_addr = Address.objects.get(id=user.addr_id)
    except Exception as e:
        print(e)
        default_addr = None
    try:
        addrlist = Address.objects.filter(user_id=usr_id)
    except Exception as e:
        print(e)
        addrlist = None
    # 新增地址
    if request.method == 'POST' and request.POST.getlist('add_addr'):
        print(request.POST)
        # 从 form 表单获取数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        # 检验数据合法性
        # 数据缺失
        if not all([receiver, addr, zip_code, phone]):
            return render(request, 'user_center_site2.html', {'user': user, 'addrlist': addrlist, 'isLogin': isLogin,
                                                              'default_addr': default_addr, 'errmsg': '您填写的数据不全'})
        # 电话号码格式错误
        if not re.match(r'^1[3|4|5|7|8|9][0-9]{9}$', phone):
            return render(request, 'user_center_site2.html', {'user': user, 'addrlist': addrlist, 'isLogin': isLogin,
                                                              'default_addr': default_addr, "errmsg": "手机号格式不正确"})
        try:
            Address(user_id=usr_id, name=receiver, text=addr, zipcode=zip_code, tel=phone).save()
        except Exception as e:
            print(e)
        return HttpResponseRedirect('user_center_site')
    # 设置默认地址
    elif request.method == 'POST' and request.POST.getlist('select_addr'):
        print(request.POST)
        try:
            addr_id = int(request.POST.get('addr'))
            user.addr_id = addr_id
            user.save()
        except Exception as e:
            print(e)
            render(request, 'user_center_site2.html', {'user': user, 'addrlist': addrlist, 'isLogin': isLogin,
                                                       'default_addr': default_addr, "errmsg": "设置默认地址失败"})
        return HttpResponseRedirect('user_center_site')
    # 删除地址
    elif request.method == 'POST':
        print(request.POST)
        addr_id = int(json.loads(request.body.decode("utf-8")).get('id', -1))
        try:
            Address.objects.filter(id=addr_id).delete()
        except Exception as e:
            print(e)
            return render(request, 'user_center_site2.html', {'user': user, 'addrlist': addrlist, 'isLogin': isLogin,
                                                              'default_addr': default_addr, "errmsg": "删除失败"})
        print('redirect')
        return HttpResponseRedirect('user_center_site')
    # GET 请求
    return render(request, 'user_center_site2.html',
                  {'default_addr': default_addr, 'user': user, 'addrlist': addrlist, 'isLogin': isLogin})


def merchant_register_view(request):
    # 获取cookies里的当前登录用户id
    usr_id = int(request.session.get('uid', -1))
    isLogin = usr_id != -1
    # 若用户未登录
    if not isLogin:
        return render(request, 'merchant_login.html', {'errmsg': '请先登录'})
    # 访问商家注册页
    if request.method == 'GET':
        # 检测商家状态
        state = User.objects.get(id=usr_id).is_merchant
        if state == 0:  # 未注册
            return render(request, 'merchant_register.html')
        elif state == 1:  # 待审核
            return render(request, 'merchant_register.html', {'errmsg': "is_merchant = 1\n待管理员审核通过"})
        elif state == 2:  # 若已经是商家
            # 给出提示
            return HttpResponseRedirect('merchant')
        else:
            return render(request, 'merchant_register.html', {'errmsg': "is_merchant = {}\n状态错误，请联系管理员".format(state)})
    # 提交注册请求
    elif request.method == 'POST':
        # 获取当前登录用户uid
        usr_id = int(request.session.get('uid'))
        # 若 usr_id不存在或为默认值，则应该报错
        if not usr_id:
            return HttpResponseRedirect('err_handling_page')  # not defined
        # 从 form 表单获取数据
        shop_name = request.POST.get('shop_name')
        text = request.POST.get('text')
        create_money = request.POST.get('create_money')
        allow = request.POST.get('allow')
        # 数据缺失
        if not all([shop_name, text, create_money]):
            return render(request, 'merchant_register.html', {'errmsg': '您填写的数据不全'})
        # 必须勾选用户协议
        if allow != 'on':
            return render(request, 'merchant_register.html', {'errmsg': '请您先勾选同意协议'})
        try:
            Shop(user_id=usr_id, name=shop_name, text=text, create_money=int(create_money),
                 access_times=0, mark=0, total_income=0).save()
            User.objects.filter(id=usr_id).update(is_merchant=1)  # 设置商家申请状态，提交给管理员审核
        except Exception as e:
            print(e)
            # 提交申请失败
            return render(request, 'merchant_register.html', {'errmsg': e})
        return HttpResponseRedirect('merchant_register')


def merchant_login_view(request):
    if request.method == 'GET':
        return render(request, 'merchant_login.html', {})
    elif request.method == 'POST':
        # 处理数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        # 校验数据
        if not all([username, password]):
            return render(request, 'merchant_login.html', {'errmsg': '数据不完整'})
        try:
            user = User.objects.get(name=username)
        except Exception as e:
            print('--login user error %s' % e)
            return render(request, 'register.html', {'errmsg': '您的用户名未进行注册'})
        # 比对密码
        m = hashlib.md5()
        m.update(password.encode())

        if m.hexdigest() != user.pwd:
            print("密码错误", m.hexdigest())
            return render(request, 'merchant_login.html', {'errmsg': '您的用户名和密码有错误'})
        # 记录会话状态
        request.session['username'] = username
        request.session['uid'] = user.id
        request.session['userimg'] = user.img
        return HttpResponseRedirect('merchant')


def merchant_view(request):
    # 获取cookies里的当前登录用户id
    usr_id = int(request.session.get('uid', -1))
    isLogin = usr_id != -1
    # 若用户未登录
    if not isLogin:
        return HttpResponseRedirect('login')  # not defined
    # 检测是否商家
    if User.objects.get(id=usr_id).is_merchant != 2:
        return HttpResponseRedirect('merchant_register')
    # 获取数据
    user = User.objects.get(id=usr_id)
    shop = Shop.objects.get(user_id=usr_id)
    return render(request, "merchant2.html", {'isLogin': isLogin, 'user': user, 'shop': shop})

# 初级分页
def page(num,size=10):
    # 接受页码
    num = int(num)
    # 获取总个数
    totalRecords = Goods.objects.count()
    # 总页数
    totalPages = int(math.ceil(totalRecords*1.0/size));
    # 是否越界
    if num<1:
        num = 1
    if num>totalPages:
        num = totalPages
    showGoods = Goods.objects.all()[((num-1)*size):(num*size)]
    return showGoods,num

def merchant_object_view(request):
    # 获取cookies里的当前登录用户id
    usr_id = int(request.session.get('uid', -1))
    isLogin = usr_id != -1
    # 若用户未登录
    if not isLogin:
        return HttpResponseRedirect('login')  # not defined
    # 检测是否商家
    if User.objects.get(id=usr_id).is_merchant != 2:
        return HttpResponseRedirect('merchant_register')

    # 分页功能

    m = request.method
    # GET请求， 加载页面
    if m == 'GET':
        page_num = int(request.GET.get('pnum',1))
        goodsList = []
        # 获取数据
        # totalRecords = Goods.objects.all()
        user = User.objects.get(id=usr_id)
        shop = Shop.objects.get(user_id=usr_id)
        totalRecords = Goods.objects.filter(shop_id=shop.id)
        pager = Paginator(totalRecords,10)
        try:
            perpage_data = pager.page(page_num)
        except PageNotAnInteger:
            perpage_data = pager.page(1)
        except EmptyPage:
            perpage_data = pager.page(pager.num_pages)

        begin = (page_num-int(math.ceil(10.0/2)))
        if begin < 1:
            begin = 1
        end = begin + 9
        if end > pager.num_pages:
            end = pager.num_pages
        if end <= 10:
            begin = 1
        else:
            begin = end - 9
        pagelist = range(begin,end+1)
        return render(request, 'merchant_object.html',
                      {'isLogin': isLogin, 'user': user, 'shop': shop, 'perpage_data': perpage_data,'pagelist':pagelist,'now_page':page_num})
    # try:
    #     tmp = Goods.objects.filter(shop_id=shop.id)
    #     goodsList = []
    #     for good in tmp:
    #         _ = good.__dict__
    #         orders = Order.objects.filter(goods_id=good.id)
    #         deal = 0
    #         for order in orders:
    #             deal += order.goods_num
    #         _['deal'] = deal
    #         goodsList.append(_)
    # except:
    #     goodsList = None
    if request.method == 'POST':
        gid = int(json.loads(request.body.decode("utf-8")).get('id'))
        flag = json.loads(request.body.decode("utf-8")).get('flag')
        try:
            if flag == 'updatenum':
                Goods.objects.filter(id=gid).update(number=
                                                    int(json.loads(request.body.decode("utf-8")).get('num')))
            elif flag == 'updateprice':
                Goods.objects.filter(id=gid).update(price=
                                                    int(json.loads(request.body.decode("utf-8")).get('price')))
            elif flag == 'puton':
                # 更改数量啥的
                Goods.objects.filter(id=gid).update(status=1)  # 设置为上架
            elif flag == 'putoff':
                # 更改数量啥的
                Goods.objects.filter(id=gid).update(status=0)  # 设置为下架
                print('put off')
            return JsonResponse({})
        except Exception as e:
            print(e)
            return HttpResponseRedirect('merchant_object')
    return render(request, 'merchant_object.html',
                  {'isLogin': isLogin, 'user': user, 'shop': shop, 'goodsList': goodsList})


def merchant_order_view(request):
    # 获取cookies里的当前登录用户id
    usr_id = int(request.session.get('uid', -1))
    isLogin = usr_id != -1
    # 若用户未登录
    if not isLogin:
        return HttpResponseRedirect('err_handling_page')  # not defined
    # 检测是否商家
    if User.objects.get(id=usr_id).is_merchant != 2:
        return render(request, 'merchant_register.html')
    # 获取数据
    user = User.objects.get(id=usr_id)
    shop = Shop.objects.get(user_id=usr_id)
    try:
        orderList = cart.orderlist_response.getOrderList_shopvision(shop.id)
    except:
        orderList = None
    if request.method == 'POST':
        # 完成发货
        oid = int(json.loads(request.body.decode("utf-8")).get('oid', -1))
        Order.objects.filter(id=oid).update(delivery_state='已发货')
        print('change state')
        return HttpResponseRedirect('merchant_order')
    return render(request, 'merchant_order.html',
                  {'isLogin': isLogin, 'user': user, 'orderList': orderList, 'shop': shop})


def manager_view(request):
    usr_id = int(request.session.get('uid', -1))
    isLogin = usr_id != -1
    # 若用户未登录
    if not isLogin:
        return HttpResponseRedirect('err_handling_page')  # not defined
    # 检测是否是管理员
    isManager = User.objects.get(id=usr_id).is_merchant == 3
    # 获取申请人的信息
    user = User.objects.get(id=usr_id)
    shopList = Shop.objects.all()
    if request.method == 'GET':
        # 根据申请时间
        # 在提交商家注册的时候要把updatetime加上去
        applyList = User.objects.filter(is_merchant__in=[1, 2]).order_by('is_merchant')
        applySuccessList = User.objects.filter(is_merchant=2).order_by('updatetime')
        return render(request, 'user_center_manager.html',
                      {'isLogin': isLogin,
                       'shopList': shopList,
                       'user': user,
                       'applyList': applyList,
                       'applySuccessList': applySuccessList,
                       })
    else:  # 接受ajax请求，同意申请
        print("响应POST请求")
        data = request.body.decode("utf-8")
        json_data = json.loads(data)
        print(json_data)
        aid = int(json_data.get('aid', -1))
        print(aid)
        User.objects.filter(id=aid).update(is_merchant=2)
        return JsonResponse({"res": 1})

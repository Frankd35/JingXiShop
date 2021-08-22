import hashlib
import re
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
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
        return HttpResponseRedirect('/index')


def login_view(request):
    if request.method == 'GET':
        # 获取登录页面
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect('/index')
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
            return HttpResponseRedirect('/index')
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
            return HttpResponse('您的用户名或者密码有错误')
        # 比对密码
        m = hashlib.md5()
        m.update(password.encode())

        if m.hexdigest() != user.pwd:
            print("密码错误",m.hexdigest())
            return render(request, 'login.html', {'errmsg': '您的用户名和密码有错误'})
        # 记录会话状态
        request.session['username'] = username
        request.session['uid'] = user.id
        request.session['userimg'] = user.img
        resp = HttpResponseRedirect('index')
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
    resp = HttpResponseRedirect('/index')
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
        return HttpResponseRedirect('err_handling_page')  # not defined
    user = User.objects.get(id=usr_id)
    # address 选择实现
    return render(request, 'user_center_info2.html', {'user': user, 'address': None, 'isLogin': isLogin})


def usr_site_view(request):
    # 获取cookies里的当前登录用户id
    usr_id = int(request.session.get('uid', -1))
    isLogin = usr_id != -1
    # 若用户未登录
    if not isLogin:
        return HttpResponseRedirect('err_handling_page')  # not defined
    # 若为地址修改请求，则处理修改请求
    if request.method == 'POST':
        receiver = request.POST.get('receiver')
        addr = request.POST.get('text')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        # 数据缺失
        if not all([receiver, addr, zip_code,phone]):
            # 未实现的报错接口
            return render(request, 'usr_site_view.html', {'errmsg': '您填写的数据不全'})
        try:
            Address(user_id=usr_id, name=receiver, text=addr, zipcode=zip_code, tel=phone).save()
        except Exception as e:
            print(e)
    user = User.objects.get(id=usr_id)
    try:
        address = Address.objects.filter(user_id=usr_id).first()
    except Exception as e:
        address = None
    return render(request, 'user_center_site2.html', {'user': user, 'address': address, 'isLogin': isLogin})


def merchant_register_view(request):
    # 访问商家注册页
    if request.method == 'GET':
        # 若已经是商家 给出提示
        return render(request, 'merchant_register.html')
    # 提交注册请求
    elif request.method == 'POST':
        # 获取当前登录用户uid
        usr_id = int(request.session.get('uid'))
        # 若 usr_id不存在或为默认值，则应该报错
        if not usr_id:
            return HttpResponseRedirect('err_handling_page')  # not defined
        # 若已经是商家则直接进入商家界面
        elif User.objects.get(id=usr_id).is_merchant:
            return HttpResponseRedirect('merchant')
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

        Shop(user_id=usr_id, name=shop_name, text=text, create_money=int(create_money), access_times=0).save()
        return render(request, 'merchant_register.html')

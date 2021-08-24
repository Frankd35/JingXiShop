"""WebProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.http import HttpResponseRedirect
from user import views as usr_views
from cart import views as c_views
from index import views as in_views
from goods import views as goods_views
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # 设置初始跳转
    path(r'', lambda req: HttpResponseRedirect('/index')),
    path('admin/', admin.site.urls),
    # cart 模块路由转发
    path('order', c_views.orderplace_view),
    path('cart', c_views.cart_view),
    path('favorite', c_views.collect_view),
    path('user_center_order',c_views.orderlist_view),
    # index 模块路由转发
    path('index', in_views.index_view),
    path('index_template', in_views.index_template_view),
    # user 模块路由转发
    path('register', usr_views.reg_view, name='register'),
    path('login', usr_views.login_view),
    path('logout', usr_views.logout_view),
    path('user_center_info2', usr_views.usr_info_view),
    path('user_center_site2', usr_views.usr_site_view),
    path('merchant_register', usr_views.merchant_register_view),
    path('merchant', usr_views.merchant_view),



    # goods 模块路由转发
    path('detail_template', goods_views.detail_view),

    # path('logout', views.logout_view)

    # path('user/', include('user.urls')),

    # url(r'index/',include('index.urls')),
]

# 设置静态文件路径
urlpatterns += staticfiles_urlpatterns()

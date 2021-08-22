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

from user import views
from cart import views as c_views
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart', c_views.cart_view),
    path('favorite', c_views.collect_view),
    path('orderplace', c_views.orderplace_view),

    path('register', views.reg_view, name='register'),
    path('login', views.login_view),
    # path('logout', views.logout_view)

    # path('user/', include('user.urls')),

    # url(r'index/',include('index.urls')),
]

# 设置静态文件路径
urlpatterns += staticfiles_urlpatterns()

from django.http import HttpResponse
from django.shortcuts import render
from goods import models as goods_model
from user import models as user_model
from cart import models as cart_model


class ShowGoods:
    def __init__(self, gid, name, img, num, price, shopName, tttprice=0):
        self.gid = gid
        self.name = name
        self.img = img
        self.num = num
        self.price = price
        self.shopName = shopName
        self.sum = price * num
        self.tttprice = tttprice


class ListInt:
    def __init__(self, goodsList, total_price):
        self.goodsList = goodsList
        self.total_price = total_price


def dealRequest(user_id, flag, gid, isChosen):
    if user_id == -1:
        return []
    goodsList = []
    # 根据user_id获取用户信息
    tempList = cart_model.Cart.objects.filter(user_id=user_id)
    total_price = 0
    print("flag=" + str(flag))
    if flag == 0:
        # 每次进入页面（GET 请求）重置is_chosen为0
        cart_model.Cart.objects.filter(user_id=user_id).update(is_chosen=0, goods_num=0)
        print("GET请求重置")
    elif flag == 1:  # 选中 or 不选中
        if isChosen:  # 该商品被选中
            cart_model.Cart.objects.filter(user_id=user_id, goods_id=gid).update(is_chosen=1)
            print("商品选中")
        else:  # 该商品未被选中
            cart_model.Cart.objects.filter(user_id=user_id, goods_id=gid).update(is_chosen=0)
            print("商品取消选中")
        return []
    elif flag == 2:  # 增加
        max_num = goods_model.Goods.objects.filter(id=gid).first().number
        target_num = cart_model.Cart.objects.filter(user_id=user_id, goods_id=gid).first().goods_num + 1
        if target_num > max_num:
            print("可选商品商量达到上限")
        cart_model.Cart.objects.filter(user_id=user_id, goods_id=gid).update(goods_num=min(max_num, target_num))
        print("商品增加")
        return []
    elif flag == 3:  # 减少
        ori_num = cart_model.Cart.objects.filter(user_id=user_id, goods_id=gid).first().goods_num
        if ori_num > 1:
            cart_model.Cart.objects.filter(user_id=user_id, goods_id=gid).update(goods_num=(ori_num - 1))
        print("商品减少")
        return []
    elif flag == 4:  # 删除
        cart_model.Cart.objects.filter(user_id=user_id, goods_id=gid).first().delete()
        print("商品删除")
        return []
    elif flag == 5:  # 全选 or 取消全选
        if isChosen:
            cart_model.Cart.objects.filter(user_id=user_id).update(is_chosen=1)
            print("全选")
        else:
            cart_model.Cart.objects.filter(user_id=user_id).update(is_chosen=0)
            print("取消全选")
        return []
    for i in tempList:
        tempGoods = goods_model.Goods.objects.filter(id=i.goods_id).first()
        tempShop = user_model.User.objects.filter(id=i.shop_id).first()
        tempShopName = ""
        if tempShop:
            tempShopName = tempShop.name
        tempName = tempGoods.name
        tempImg = tempGoods.img
        tempPrice = tempGoods.price
        if i.is_chosen != 0:
            total_price += i.goods_price * i.goods_num
        hhh = ShowGoods(i.goods_id, tempName, tempImg, i.goods_num, tempPrice, tempShopName, total_price)
        goodsList.append(hhh)
        print("name:%s,img:%s,num:%d,price:%f,shopName:%s" % (hhh.name, hhh.img, hhh.num, hhh.price, hhh.shopName))

    return goodsList

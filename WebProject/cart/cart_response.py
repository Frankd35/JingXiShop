from django.http import HttpResponse
from django.shortcuts import render
from goods import models as goods_model
from user import models as user_model
from cart import models as cart_model


class ShowGoods:
    def __init__(self, gid, name, img, num, price, shopName):
        self.gid = gid
        self.name = name
        self.img = img
        self.num = num
        self.price = price
        self.shopName = shopName
        self.sum = price * num


def dealRequest(user_id, flag, gid, isChosen):
    if user_id == -1:
        return []
    goodsList = []
    # 根据user_id获取用户信息
    tempList = cart_model.Cart.objects.filter(user_id=user_id)
    total_price = 0
    if flag == 0:
        # 每次进入页面（GET 请求）重置is_chosen为0
        cart_model.Cart.objects.filter(user_id=user_id).update(is_chosen=0)
    elif flag == 1:  # 选中 or 不选中
        if isChosen:  # 该商品被选中
            cart_model.Cart.objects.filter(user_id=user_id, goods_id=gid).update(is_chosen=1)
        else:  # 该商品未被选中
            cart_model.Cart.objects.filter(user_id=user_id, goods_id=gid).update(is_chosen=0)
    for i in tempList:
        tempGoods = goods_model.Goods.objects.filter(id=i.goods_id)[0]
        # 从数据库获取店铺信息
        tempShopName = '哈哈哈店铺'
        tempName = tempGoods.name
        tempImg = tempGoods.img
        hhh = ShowGoods(i.goods_id, tempName, tempImg, i.goods_num, i.goods_price, tempShopName)
        if i.is_chosen != 0:
            total_price += hhh.sum
        goodsList.append(hhh)
        print("name:%s,img:%s,num:%d,price:%f,shopName:%s" % (hhh.name, hhh.img, hhh.num, hhh.price, hhh.shopName))

    return goodsList, total_price


def deleteGoods(uid, gid):
    # books=models.Book.objects.filter(pk=8).first().delete()

    return None

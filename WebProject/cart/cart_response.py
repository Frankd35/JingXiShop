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


def dealRequest(user_id):
    goodsList = []
    tempList = cart_model.Cart.objects.filter(user_id=user_id)
    for i in tempList:
        tempGoods = goods_model.Goods.objects.filter(id=i.goods_id)[0]
        # tempShop =
        tempShopName = '哈哈哈店铺'
        tempName = tempGoods.name
        tempImg = tempGoods.img
        hhh = ShowGoods(i.goods_id, tempName, tempImg, i.goods_num, i.goods_price, tempShopName)
        goodsList.append(hhh)
        print("name:%s,img:%s,num:%d,price:%f,shopName:%s"%(hhh.name, hhh.img, hhh.num, hhh.price, hhh.shopName))

    return goodsList

from django.http import HttpResponse
from django.shortcuts import render
from goods import models as goods_model
from user import models as user_model
from cart import models as cart_model


class TempCollect:
    def __init__(self, name, goods_id, img, price, shopName):
        self.name = name
        self.goods_id = goods_id
        self.img = img
        self.price = price
        self.shopName = shopName


def collectRequest(user_id):
    if user_id == -1:
        return []
    goodsList = []
    tempCollectList = cart_model.Favorite.objects.filter(user_id=user_id)
    for i in tempCollectList:
        tempGoods = goods_model.Goods.objects.filter(id=i.goods_id).first()
        tempShop = user_model.Shop.objects.filter(id=tempGoods.shop_id).first()
        tempCollectObj = TempCollect(tempGoods.name, tempGoods.id, tempGoods.img, tempGoods.price, tempShop.name)
        goodsList.append(tempCollectObj)
        print("Shop name: %s, Goods name: %s" % (tempCollectObj.shopName, tempCollectObj.name))

    return goodsList


def deleteCollect(user_id, goods_id):
    cart_model.Favorite.objects.filter(user_id=user_id, goods_id=goods_id).delete()

    return None

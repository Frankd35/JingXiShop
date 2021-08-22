from django.http import HttpResponse
from django.shortcuts import render
from goods import models as goods_model
from user import models as user_model
from cart import models as cart_model

class showGoods:
    def __init__(self,name,img,num,shop,price):
        self.name = name
        self.img = img
        self.num = num
        self.shop = shop
        self.price = price


def dealRequest(user_id):
    # tempList = cart_model.Cart.objects.all()
    tempList = user_model.User.objects.filter(id=user_id)
    for i in tempList:
        print("hhh:"+str(i.id))

    print(tempList)

    goodsList = []

    return goodsList

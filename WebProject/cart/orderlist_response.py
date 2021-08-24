from django.http import HttpResponse
from django.shortcuts import render
from goods import models as goods_model
from user import models as user_model
from cart import models as cart_model


class TempOrder:
    def __init__(self, name, img, price, num, addr, state, order_id, time, total_price, per_name=""):
        self.name = name
        self.img = img
        self.price = price
        self.num = num
        self.addr = addr
        self.state = state
        self.order_id = order_id
        self.time = time
        self.total_price = total_price
        self.per_name = per_name


def getOrderList(user_id):
    orderList = []
    tempOrderList = cart_model.Order.objects.filter(user_id=user_id)
    for i in tempOrderList:
        tempGoods = goods_model.Goods.objects.filter(id=i.goods_id).first()
        orderList.append(TempOrder(tempGoods.name, tempGoods.img, tempGoods.price, i.goods_num, i.addr, i.delivery_state, i.id, i.trade_time, i.total_price, i.per_name))

    return orderList


def getOrderList_shopvision(shop_id):
    orderList = []
    tempOrderList = cart_model.Order.objects.filter(shop_id=shop_id)
    for i in tempOrderList:
        tempGoods = goods_model.Goods.objects.filter(id=i.goods_id).first()
        orderList.append(TempOrder(tempGoods.name, tempGoods.img, tempGoods.price
                                   , i.goods_num, i.addr, i.delivery_state, i.id, i.trade_time, i.total_price, i.per_name))
    # print(orderList)
    return orderList
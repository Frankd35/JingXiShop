from cart import models as cart_model
from goods import models as goods_model
from user import models as user_model


class tempOrderGoods:
    def __init__(self, name, price, num, tttprice=0):
        self.name = name
        self.price = price
        self.num = num
        self.total_price = price * num
        self.tttprice = tttprice


def OrderPlaceRequest(user_id):
    total_price = 0
    if user_id == -1:
        return []
    goodsList = []
    tempCartList = cart_model.Cart.objects.filter(user_id=user_id, is_chosen=1, goods_num__gt=0)
    for i in tempCartList:
        tempGoods = goods_model.Goods.objects.filter(id=i.goods_id)[0]
        tempName = tempGoods.name
        total_price += i.goods_price * i.goods_num
        goodsList.append(tempOrderGoods(tempName, i.goods_price, i.goods_num, total_price))

    return goodsList

def GetAddr(user_id):
    if user_id == -1:
        return []
    addr = user_model.Address.objects.filter(user_id=user_id)
    return addr

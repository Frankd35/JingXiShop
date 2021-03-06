from cart import models as cart_model
from goods import models as goods_model
from user import models as user_model


class tempOrderGoods:
    def __init__(self, name, price, num, img, tttprice=0):
        self.name = name
        self.price = price
        self.num = num
        self.total_price = price * num
        self.img = img
        self.tttprice = tttprice


# class tempAddr:
#     def __init__(self, ):


def OrderPlaceRequest(user_id):
    total_price = 0
    if user_id == -1:
        return []
    goodsList = []
    tempCartList = cart_model.Cart.objects.filter(user_id=user_id, is_chosen=1, goods_num__gt=0)
    for i in tempCartList:
        tempGoods = goods_model.Goods.objects.filter(id=i.goods_id).first()
        tempName = tempGoods.name
        tempImg = tempGoods.img
        tempPrice = tempGoods.price
        total_price += tempPrice * i.goods_num
        goodsList.append(tempOrderGoods(tempName, tempPrice, i.goods_num, tempImg, total_price))

    return goodsList


def GetAddr(user_id):
    if user_id == -1:
        return []
    addr = user_model.Address.objects.filter(user_id=user_id)
    return addr


def settleOrder(user_id, addr_id):
    tempAddr = user_model.Address.objects.filter(id=addr_id).first()
    tempOrderList = cart_model.Cart.objects.filter(user_id=user_id, is_chosen=1, goods_num__gt=0)
    for i in tempOrderList:
        tempGoods = goods_model.Goods.objects.filter(id=i.goods_id).first()
        tempPrice = tempGoods.price * i.goods_num + 10
        shopId = goods_model.Goods.objects.filter(id=i.goods_id).first().shop_id
        cart_model.Order.objects.create(user_id=user_id, shop_id=shopId, goods_id=i.goods_id, goods_num=i.goods_num, total_price=tempPrice, addr=tempAddr.text, pay_state=1, delivery_state="未发货", per_name=tempAddr.name)
        goods_model.Goods.objects.filter(id=i.goods_id).update(number=max(0, (tempGoods.number-i.goods_num))) # 商品库存减少
        cart_model.Cart.objects.filter(user_id=user_id, goods_id=i.goods_id).delete()
        print("哈哈哈settle成功: 商品%s" % i.goods_id)

    return None


def setDefaultAddr(user_id, addr_id):
    user_model.User.objects.filter(id=user_id).update(addr_id=addr_id)
    return None

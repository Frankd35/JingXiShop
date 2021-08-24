from goods import models as goods_model
from user import models as user_model
from cart import models as cart_model


class TempComment:
    def __init__(self, user_name, user_img, mark, text, createtime):
        self.user_name = user_name
        self.user_img = user_img
        self.mark = mark
        self.text = text
        self.createtime = createtime


def getGoodsDetail(goods_id):
    goods = goods_model.Goods.objects.filter(id=goods_id).first()
    return goods


def getShopDetail(shop_id):
    shop = user_model.Shop.objects.filter(id=shop_id).first()
    return shop


def getCommentList(goods_id):
    tempList = []
    commentList = goods_model.Comment.objects.filter(goods_id=goods_id)
    for i in commentList:
        tempUser = user_model.User.objects.filter(id=i.user_id).first()
        tempList.append(TempComment(tempUser.name, tempUser.img, i.mark, i.text, i.createtime))
    return tempList


def buyNow(uid, gid, num):
    cart_model.Cart.objects.all().update(is_chosen=0)
    tempGoods = goods_model.Goods.objects.filter(id=gid).first()
    if cart_model.Cart.objects.filter(user_id=uid, goods_id=gid).count() > 0:
        cart_model.Cart.objects.filter(user_id=uid, goods_id=gid).update(goods_num=num, is_chosen=1)
    else:
        cart_model.Cart.objects.create(user_id=uid, shop_id=tempGoods.shop_id, goods_id=gid,
                                       goods_price=tempGoods.price,
                                       goods_num=num, goods_img=tempGoods.img, is_chosen=1)
    return None


def addCart(uid, gid, num):
    tempGoods = goods_model.Goods.objects.filter(id=gid).first()
    if cart_model.Cart.objects.filter(user_id=uid, goods_id=gid).count() > 0:
        cart_model.Cart.objects.filter(user_id=uid, goods_id=gid).update(goods_num=num)
    else:
        cart_model.Cart.objects.create(user_id=uid, shop_id=tempGoods.shop_id, goods_id=gid,
                                       goods_price=tempGoods.price,
                                       goods_num=num, goods_img=tempGoods.img, is_chosen=0)
    return None


def addCollect(uid, gid):
    tempGoods = goods_model.Goods.objects.filter(id=gid).first()
    if cart_model.Favorite.objects.filter(user_id=uid, goods_id=gid).count() < 1:
        cart_model.Favorite.objects.create(user_id=uid, goods_id=gid, goods_img=tempGoods.img)
    return None

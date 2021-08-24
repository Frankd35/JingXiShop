from goods import models as goods_model
from user import models as user_model
from cart import models as cart_model


def getGoodsDetail(goods_id):
    goods = goods_model.Goods.objects.filter(id=goods_id).first()
    return goods


def getShopDetail(shop_id):
    shop = user_model.Shop.objects.filter(id=shop_id).first()
    return shop


def getCommentList(goods_id):
    commentList = goods_model.Comment.objects.filter(goods_id=goods_id)
    return commentList

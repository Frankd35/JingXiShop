from django.db import models


# Create your models here.

# 购物车
class Cart(models.Model):
    user_id = models.IntegerField()
    shop_id = models.IntegerField(blank=True)
    goods_id = models.IntegerField()
    goods_price = models.DecimalField(max_digits=10, decimal_places=4, blank=True)
    goods_num = models.IntegerField()
    goods_img = models.CharField(max_length=200, blank=True)
    is_chosen = models.IntegerField(default=0)

    def __str__(self):
        return u"User:%s's cart" % self.user_id


# 收藏夹
class Favorite(models.Model):
    user_id = models.IntegerField()
    goods_id = models.IntegerField()
    goods_img = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return u"%s like %s" % (self.user_id, self.goods_id)


# 订单
class Order(models.Model):
    user_id = models.IntegerField()
    shop_id = models.IntegerField(blank=True)
    goods_id = models.IntegerField()
    goods_num = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=4)
    trade_time = models.DateField(auto_now_add=True)
    addr = models.CharField(max_length=200, blank=True)
    pay_state = models.IntegerField(blank=True)
    delivery_state = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return u"%s's oder: %s" % (self.user_id, self.goods_id)

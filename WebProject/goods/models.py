from django.db import models


# Create your models here.
class Goods(models.Model):
    category_id = models.IntegerField()
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    number = models.IntegerField()
    img = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    status = models.IntegerField(default=0)
    shop_id = models.IntegerField()
    searching_num = models.IntegerField()

    def __str__(self):
        return u"Shop:%s's goods%s" % (self.shop_id, self.name)

class Category(models.Model):
    name = models.CharField(max_length=200)
    state = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return u"Category : %s" % self.name

class Comment(models.Model):
    user_id = models.IntegerField()
    goods_id = models.IntegerField()
    text = models.TextField()
    mark = models.DecimalField(max_digits=10, decimal_places=2, default=5.00, blank=True)
    createtime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"Comment : User %d -> Goods %d", (self.user_id, self.goods_id)

from django.db import models


# Create your models here.
class Goods(models.Model):
    category_id = models.IntegerField()
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    number = models.IntegerField()
    img = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    status = models.IntegerField(default=0)
    shop_id = models.IntegerField()
    searching_num = models.IntegerField()

    def __str__(self):
        return u"Shop:%s's goods%s" % (self.shop_id, self.name)

from django.db import models


# Create your models here.

class User(models.Model):
    img = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, unique=True)
    pwd = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    createtime = models.DateField(auto_now=True)
    updatetime = models.DateField(auto_now_add=True)
    is_merchant = models.BooleanField(default=False)

    def __str__(self):
        return u"User:%s's name" % self.name


class Address(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=20)
    tel = models.CharField(max_length=20)

    def __str__(self):
        return u"user id:%d\tname:%s\ttext:%s\tzipcode:s%\ttelphone:s%" % \
               (self.user_id, self.name, self.text, self.zipcode, self.tel)


class Shop(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=200,unique=True)
    text = models.CharField(max_length=200)
    img = models.CharField(max_length=200, blank=True)
    mark = models.IntegerField()
    total_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    access_times = models.IntegerField()
    creattime = models.DateField(auto_now=True)

    def __str__(self):
        return u"%s's shop: %s" % (User.object.get(id=self.user_id).name, self.name)
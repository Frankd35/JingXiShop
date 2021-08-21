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

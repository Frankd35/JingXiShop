from django.contrib import admin

# Register your models here.
from django.contrib import admin
# Register your models here.
from .models import *

admin.site.register(Goods)
admin.site.register(Category)
admin.site.register(Comment)
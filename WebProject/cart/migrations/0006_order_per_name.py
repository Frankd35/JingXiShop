# Generated by Django 3.2.6 on 2021-08-23 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_alter_cart_goods_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='per_name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]

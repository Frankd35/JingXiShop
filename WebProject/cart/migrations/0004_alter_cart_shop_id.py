# Generated by Django 3.2.6 on 2021-08-21 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_auto_20210821_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='shop_id',
            field=models.IntegerField(blank=True),
        ),
    ]

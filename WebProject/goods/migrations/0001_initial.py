# Generated by Django 3.2.6 on 2021-08-21 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=4, max_digits=10)),
                ('number', models.IntegerField()),
                ('img', models.CharField(max_length=200)),
                ('text', models.TextField(blank=True)),
                ('status', models.IntegerField(default=0)),
                ('shop_id', models.IntegerField()),
                ('searching_num', models.IntegerField()),
            ],
        ),
    ]

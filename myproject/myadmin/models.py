from django.db import models

# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=20,unique=True)
    age = models.IntegerField(null=True)
    password = models.CharField(max_length=80)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=20,null=True)
    sex = models.CharField(max_length=20,null=True)
    pic = models.CharField(max_length=200,null=True)
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'


class Types(models.Model):
    typename = models.CharField(max_length=40)
    pid = models.IntegerField()
    path = models.CharField(max_length=100)

    class Meta:
        db_table = 'types'


class Goods(models.Model):
    typeid = models.ForeignKey(to='Types',to_field='id')
    title = models.CharField(max_length=100)
    #商品描述
    descr = models.CharField(max_length=200,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pics = models.CharField(max_length=80)
    #商品详情
    info = models.TextField(null=True)

    status = models.IntegerField(default=0)
    #库存
    store = models.IntegerField(default=0)
    #购买数量
    num = models.IntegerField(default=0)

    clicknum =models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:

        db_table = 'goods'


# 会员地址
class Address(models.Model):
    uid =  models.ForeignKey(to="Users", to_field="id")
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=20)
    xiangxi = models.CharField(max_length=50)
    status = models.IntegerField(default=0)

    class Meta:

        db_table = 'adress'



# 订单模型
class Orders(models.Model):
    uid = models.ForeignKey(to="Users", to_field="id")
    addressid = models.ForeignKey(to="Address", to_field="id")
    totalprice = models.FloatField()
    totalnum = models.IntegerField()
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:

        db_table = 'orders'

# 订单详情
class OrderInfo(models.Model):
    orderid = models.ForeignKey(to="Orders", to_field="id")
    gid = models.ForeignKey(to="Goods", to_field="id")
    num = models.IntegerField()

    class Meta:

        db_table = 'orderinfo'


class City(models.Model):
    name = models.CharField(max_length=50)
    upid = models.IntegerField()

    class Meta():
        db_table = 'district'
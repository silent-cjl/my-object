from django.db import models

# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=20)
    age = models.IntegerField(null=True)
    password = models.CharField(max_length=80)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    sex = models.CharField(max_length=20)
    pic = models.CharField(max_length=200,null=True)
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'


class Types(models.Model):
    typename = models.CharField(max_length=40)
    pid = models.IntegerField()
    path = models.CharField(max_length=100)

    class Mate:
        db_table = 'types'


class Goods(models.Mondel):
    gname = models.CharField(max_length=100)
    
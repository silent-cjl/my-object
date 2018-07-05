from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$',views.index,name='myhome_index'),
    #列表页
    url(r'^search/$',views.search,name='myhome_search'),
    #详情页
    url(r'^introduction/$',views.introduction,name='myhome_introduction'),
    #注册页
    url(r'^register/$',views.register,name='myhome_register'),
    #验证码
    url(r'^vcode/$',views.vcode,name='myhome_vcode'),
    #登录
    url(r'^login/$',views.login,name='myhome_login'),
    #退出登录
    url(r'^logout/$',views.logout,name='myhome_logout'),
    #添加购物车
    url(r'^addchar/$',views.addchar,name='myhome_addchar'),
    #购物车列表
    url(r'^charlist/$',views.charlist,name='myhome_charlist'),
    #删除购物车物品
    url(r'^delchar/$',views.delchar,name='myhome_delchar'),
    url(r'^editchar/$',views.editchar,name='myhome_editchar'),
    url(r'^ordercheck/$',views.ordercheck,name='myhome_ordercheck'),

    url(r'^addressedit/$', views.addressedit,name='myhome_addressedit'),
    url(r'^addressadd/$', views.addressadd,name='myhome_addressadd'),
    url(r'^cityget/$',views.cityget,name='cityget'),
    #  订单生成
    url(r'^ordercreate/$', views.ordercreate,name='myhome_ordercreate'),

    # 个人中心
    url(r'^mycenter/$', views.mycenter,name='myhome_mycenter'),
    # 我的订单
    url(r'^myorders/$', views.myorders,name='myhome_myorders'),

    url(r'^buy/$', views.buy,name='myhome_buy'),
]


from django.conf.urls import url
from . view import views,userviews,typesviews,goodsviews

urlpatterns = [
    
    url(r'^$',views.index,name='myadmin_index'),
   
    # 会员管理
    url(r'^user/add/$',userviews.add,name='myadmin_user_add'),
    url(r'^user/list/$',userviews.list,name='myadmin_user_list'),
    url(r'^user/delete/$',userviews.delete,name='myadmin_user_delete'),
    url(r'^user/edit/$',userviews.edit,name='myadmin_user_edit'),


    #分类管理
    url(r'^types/add/$',typesviews.add,name='myadmin_types_add'),
    url(r'^types/list/$',typesviews.list,name='myadmin_types_list'),
    url(r'^types/delete/$',typesviews.delete,name='myadmin_types_delete'),
    # url(r'^types/edit/$',typesviews.edit,name='myadmin_types_edit'),

    #商品管理
    url(r'^goods/add/$',goodsviews.add,name='myadmin_goods_add'),
    # url(r'^goods/list/$',goodsviews.list,name='myadmin_goods_list'),
    # url(r'^goods/delete/$',goodsviews.delete,name='myadmin_goods_delete'),
    # url(r'^goods/edit/$',goodsviews.edit,name='myadmin_goods_edit'),


]

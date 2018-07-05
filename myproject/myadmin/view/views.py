from django.shortcuts import render,reverse
from django.http import HttpResponse
from .. models import Users,OrderInfo,Orders,City,Goods
from django.contrib.auth.hashers import check_password
# Create your views here.
def index(request):
    return render(request,'myadmin/index.html')

def login(request):
    if request.method == 'GET':
        return render(request,'myadmin/login.html')

    elif request.method == 'POST':
        
        try:
            ob = Users.objects.get(username=request.POST['username'])
            # print(type(ob.status))
            if ob.status != 1:
                return HttpResponse('<script>alert("sorry,您没有操作权限！");history.back(-1)</script>')
            res = check_password(request.POST['password'],ob.password)
            if res:
                request.session['AdUser']={'uid':ob.id,'username':ob.username}
                return HttpResponse('<script>alert("登录成功");location.href="'+reverse('myadmin_index')+'"</script>')

        except:
            # 用户名错误
            pass
        
        return HttpResponse('<script>alert("用户名或密码错误");history.back(-1)</script>')
 
 # 退出登录
def logout(request):


    request.session['AdUser'] = {}

    return HttpResponse('<script>alert("退出成功");location.href="'+reverse('myadmin_index')+'"</script>')


#订单列表
def orderslist(request):

    ob = Orders.objects.all()
    for x in ob:
        s =[]
        for i in str(x.addressid.address).split(','):
                
            adds = City.objects.get(id=int(i))
            s.append(adds.name)
        s = ' '.join(s)


    # 导入中分页的方法
    from django.core.paginator import Paginator

    #实例化一个分页的对象
    proj = Paginator(ob,10)
    # print(p.page_range)
    #获取模板中的页码数
    p = request.GET.get('p',1)

    #分页后返回的列表的对象
    ulist = proj.page(p)
    #迭代的页码数
    # num = proj.page_range rand()

    #获取总的页码数
    # num = proj.num_pages 100
    num = ulist.paginator.num_pages

    return render(request,'myadmin/orderslist.html',{'data':ob,'num':num,'add':s})    


def orderinfo(request):
    uid = request.GET.get('id',None)


    ob = OrderInfo.objects.filter(orderid=uid)

    # 导入中分页的方法
    from django.core.paginator import Paginator

    #实例化一个分页的对象
    proj = Paginator(ob,10)
    # print(p.page_range)
    #获取模板中的页码数
    p = request.GET.get('p',1)

    #分页后返回的列表的对象
    ulist = proj.page(p)
    #迭代的页码数
    # num = proj.page_range rand()

    #获取总的页码数
    # num = proj.num_pages 100
    num = ulist.paginator.num_pages

    return render(request,'myadmin/orderinfo.html',{'data':ob,'num':num})

def orderedit(request):
    uid = request.GET['id']
    print('s:',uid)
    ob = Goods.objects.get(id=uid)
    print('sss:',ob.status)
    
    if ob.status == 0:

        ob.status = 1
    else:
        ob.status =0
    ob.save()
    return HttpResponse('<script>alert("修改成功");history.back(-1)</script>')
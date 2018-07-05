from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from myadmin.models import Users,Types,Goods,Address,Orders,OrderInfo,City


# Create your views here.
def index(request):
    ob = Types.objects.filter(pid=0)
    
    data=[]
    for i in ob:
        i.sub = Types.objects.filter(pid=i.id)
        for v in i.sub:
            v.gsub = Goods.objects.filter(typeid=v.id)
            data.append(v)
    return render(request,'myhome/public/base.html',{'tlist':ob,'data':data})

#列表和搜索
def search(request):
    if request.method == 'GET':
        ob = Goods.objects.all()

        data = {'data':ob}
    elif request.method == "POST":
        keysword = request.POST.get('keysword',None)
        if not keysword:
            return HttpResponse('<script>history.back(-1)</script>')
        goodslist = Goods.objects.filter(title__contains=keysword)
        count = goodslist.count()
        data = {'data':goodslist,'keys':keysword,'count':count}
    

    from django.core.paginator import Paginator
    #实例化一个分页的对象
    proj = Paginator(data['data'],12)
    # print(p.page_range)
    #获取模板中的页码数
    p = request.GET.get('p',1)
    #分页后返回的列表的对象
    ulist = proj.page(p)
    #迭代的页码数
    # num = proj.page_range rand()
    #获取总的页码数
    # num = proj.num_pages 100
    data['num'] = ulist.paginator.num_pages
    return render(request,'myhome/search.html',data)


#详情
def introduction(request):

    uid = request.GET.get('id',None)
    data = Goods.objects.get(id=uid)
    data.clicknum += 1
    data.save()
    return render(request,'myhome/introduction.html',{'goods':data})


#购物车列表
def charlist(request):
    data = request.session.get('char',None)
    # print(data)
    if data:

        data = data.values()
    return render(request,'myhome/charlist.html',{'data':data})




#添加购物车
def addchar(request):
    sid = request.GET['uid']
    num = int(request.GET['num'])
    # print(num,type(num))
    #判断购物车是存在  存在就读取出来  不存在则返回一个{}
    data = request.session.get('char',{})
    # print(data.keys())

    if sid in data.keys():
        # print(data[sid]['num'])
        data[sid]['num'] += num
        
    else:
        ob = Goods.objects.get(id=sid)
        # goods = {'title':ob.title,'price':float(ob.price),'pics':ob.pics,}
        data[sid]={'id':ob.id,'title':ob.title,'price':float(ob.price),'pics':ob.pics,'num':num} 
        # print(data)  
    request.session['char'] = data
    return HttpResponse('2')


# 删除购物车的商品
def delchar(request):
    sid = request.GET['sid']
    # 获取sessin中的购物车数据
    data = request.session['char']
    print(sid)
    del data[sid]
    print(data,type(data))

    # 把购物车重新写入session
    request.session['char'] = data 

    return HttpResponse('0')

#修改购物车中商品的数量
def editchar(request):
    sid = request.GET['sid']
    num = int(request.GET['num'])

    #在session获取购物车数据
    data = request.session['char']

    # 修改
    data[sid]['num'] = num

    # 把购物车重新写入session
    request.session['char'] = data

    return HttpResponse('0')



# 地址修改
def addressedit(request):
    aid = int(request.GET['aid'])
    uid = request.session['User']['uid']
    # 获取当前用户的所有收货地址
    print(aid)
    obs = Address.objects.filter(uid=uid)
    for x in obs:
        if x.id == aid:
            x.status = 1
        else:
            x.status = 0
        x.save()

    return HttpResponse(0)


# 地址添加
def addressadd(request):
    data = eval(request.GET['data'])
    print(data)
    data['address'] = ",".join(data['address'])
    data['uid'] = Users.objects.get(id=request.session['User']['uid'])

    # 添加地址信息
    res =  Address.objects.create(**data)

    # print(res)
    
    return HttpResponse(0)

#城市联动
def cityget(request):
    upid = request.GET.get('upid',0)

    cont = City.objects.filter(upid=upid)
    data = []
    for i in cont:
        s = {'name':i.name,'id':i.id}
        data.append(s) 
    # print(data)
    return JsonResponse(data,safe=False)


# 订单确认
def ordercheck(request):
    # 获取购物车提交的数据
    items = eval(request.GET['items'])

    data = {}
    totalprice = 0
    totalnum = 0

    for x in items:
        ob = Goods.objects.get(id=x['goodsid'])
        x['title'] = ob.title
        x['price'] = float(ob.price)
        x['pics'] = ob.pics
        # 计算总价和总数
        totalprice += x['num']*x['price']
        totalnum += x['num']

    data['totalprice'] = round(totalprice,2)
    data['totalnum'] = totalnum
    data['items'] = items

    # 把确认的商品信息.,存入session
    request.session['order'] = data
    # 需要获取当前用户的收货地址
    addlist = Address.objects.filter(uid=request.session['User']['uid'])

    
    
    for i in addlist:
        s =[]     
        ap = str(i.address).split(',')
        for x in ap:
            adds = City.objects.get(id=int(x))
            s.append(adds.name)
        s = ' '.join(s)
        i.address = s
    
    
    context = {'data':data,'addlist':addlist}

    return render(request,'myhome/ordercheck.html',context)

# 生成订单
def ordercreate(request):

    # 接受用户id
    uid = request.session['User']['uid']
    print('uid')
    # 收货地址id
    addressid = request.POST['addressid']
    # 商品信息
    data = request.session['order']

    # 获取购物车中的数据
    cart = request.session['char']
    
    # 生成订单
    ob = Orders()
    ob.uid = Users.objects.get(id=uid)
    ob.addressid = Address.objects.get(id=addressid)
    ob.totalprice = data['totalprice']
    ob.totalnum = data['totalnum']
    ob.save()

    # .订单详情
    for v in data['items']:
     
        oinfo = OrderInfo()
        oinfo.orderid = ob
        oinfo.gid = Goods.objects.get(id=v['goodsid'])
        oinfo.num = v['num']
        oinfo.save()
        # 在购物车中删除当前购买的商品
        del cart[v['goodsid']]


    # 清除购物车中已经下单的商品,清除order数据
    request.session['char'] = cart
    request.session['order'] = ''

    # 把生成订单id get请求到一个新的付款页面

    return HttpResponse('<script>location.href="/buy/?orderid='+str(ob.id)+'"</script>')


def buy(request):
    ob = Orders.objects.get(id=request.GET['orderid'])
    # print(ob.tatolprice)
    s =[]
    for i in str(ob.addressid.address).split(','):
            
        adds = City.objects.get(id=int(i))
        s.append(adds.name)
    s = ' '.join(s)
        
    return render(request,'myhome/buy.html',{'data':ob,'address':s})




# 我的个人中心
def mycenter(request):
    

    return render(request,'myhome/word/index.html')

# 我的订单
def myorders(request):
    # 获取当前用户的所有订单
    data = Orders.objects.filter(uid=request.session['User']['uid'])
    
    context = {'orderlist':data}
    
    return render(request,'myhome/word/myorders.html',context)




#注册
def register(request):
    if request.method =="GET":
        return render(request,'myhome/register.html')

    elif request.method == "POST":
        #判断验证码是否正确
        if request.POST['vcode'].upper() != request.session['verifycode'].upper():
            return HttpResponse('<script>alert("验证码错误");history.back(-1)</script>')
        #接收用户提交的数据
        data = request.POST.dict()
        #删除无用的验证信息
        del(data['vcode'])
        del(data['csrfmiddlewaretoken'])
        #进行密码加密
        try:
            data['password']=make_password(data['password'],None,'pbkdf2_sha256')
            ob = Users.objects.create(**data)
            #记录用户登录的状态
            request.session['User'] = {'uid':ob.id,'username':ob.username}
            return HttpResponse('<script>alert("注册成功");location.href="/"</script>')
        # except IntegrityError:
        #     return HttpResponse('<script>alert("用户名已存在");history.back(-1)</script>')
        except:
            pass

        return HttpResponse('<script>alert("注册失败");history.back(-1)</script>')
        
# 登录
def login(request):
    if request.method == "GET":
        return render(request,'myhome/login.html')


    elif request.method == "POST":
        try:
            # print(request.POST['username'])
            ob = Users.objects.get(username=request.POST['username'])
            # print(ob)
            res = check_password(request.POST['password'],ob.password)
            # print('res')
            if res:
                request.session['User']={'uid':ob.id,'username':ob.username}
                return HttpResponse('<script>alert("登录成功");location.href="/"</script>')

        except:
            # 用户名错误
            pass
        
        return HttpResponse('<script>alert("用户名或密码错误");history.back(-1)</script>')






#验证码
def vcode(request):
    
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

# 退出登录
def logout(request):


    request.session['User'] = {}

    return HttpResponse('<script>alert("退出成功");location.href="'+reverse('myhome_index')+'"</script>')

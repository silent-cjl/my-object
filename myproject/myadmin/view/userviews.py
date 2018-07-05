from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from .. models import Users
import os
# Create your views here.

def list(request):

    types = request.GET.get('type',None)
    keywords = request.GET.get('keywords',None)
    
    if bool(types) == True and bool(keywords) == True:

        if types == "all":

            from django.db.models import Q
            obj = Users.objects.filter(
                    Q(id__contains=keyswords)|
                    Q(username__contains=keyswords)|
                    Q(age__contains=keyswords)|
                    Q(sex__contains=keyswords)|
                    Q(email__contains=keyswords)|
                    Q(status__contains=keyswords)
                )
        elif types == "id":
            obj = Users.objects.filter(id__contains=keywords)

        elif types == "username":
            obj = Users.objects.filter(username__contains=keywords)

        elif types == "age":
            obj = Users.objects.filter(age__contains=keywords)

        elif types == "sex":
            obj = Users.objects.filter(sex__contains=keywords)

        elif types == "email":
            obj = Users.objects.filter(email__contains=keywords)

        elif types == "status":
            obj = Users.objects.filter(status__contains=keywords)

    else:
        obj = Users.objects.all()
    # 导入中分页的方法
    from django.core.paginator import Paginator

    #实例化一个分页的对象
    proj = Paginator(obj,10)
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

    data = {'uinfo':ulist,'num':num}
    return render(request,'myadmin/user/list.html',data)
    # return HttpResponse('1')



def add(request):

    print(request.method)

    if request.method == 'GET':
        return render(request,'myadmin/user/add.html')

    elif request.method == 'POST':
        try:
            data = request.POST.dict()
            del(data['csrfmiddlewaretoken'])
            data['password']=make_password(data['password'],None,'pbkdf2_sha256')
            s=uploads(request)
            data['pic'] = s
            obj = Users.objects.create(**data)
            return HttpResponse('<script>alert("添加成功");location.href="'+reverse("myadmin_user_list")+'"</script>')
        except:
            return HttpResponse('<script>alert("添加失败");location.href="'+reverse("myadmin_user_add")+'"</script>')

def uploads(request):
    res = request.FILES.get('pic',None)
    if not res:
        return None
    endn = res.name.split('.').pop()
    import time,random
    pname = str(time.time())+str(random.randint(1,100000))+'.'+endn

    file = open('./static/pics/'+pname,'wb+')
    for chunk in res.chunks():
        file.write(chunk)
    file.close()
    return '/static/pics/'+pname


def delete(request):
    try:
        uid = request.GET.get('uid',None)
        ob = Users.objects.get(id=uid)
        # 判断当前用户是否右头像,如果右则删除
        if ob.pic:
        #     print(ob.pic,type(ob.pic))
        #     # /static/pics/
            os.remove('.'+ob.pic)

        ob.delete()  

        data = {'msg':'删除成功','code':0}
    except:
        data = {'msg':'删除失败','code':1}

    return JsonResponse(data)

def edit(request):
    id = request.GET.get('id',None)
    obj = Users.objects.get(id=id)
    if request.method == 'GET':
        data = {'info':obj}

        return render(request,'myadmin/user/edit.html',data)

    elif request.method == 'POST':
            print(request.POST)
        # try:
            obj.username = request.POST['username']
            obj.phone = request.POST['phone']
            print(obj)
            if request.POST['age']:
                print(1)
                obj.age = request.POST['age']
            
            if request.POST['email']:
                print(3)

                obj.email = request.POST['email']
            obj.save()
            return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myadmin_user_list')+'"</script>')
        # except:
        #     return HttpResponse('<script>alert("修改失败");location.href="'+reverse('myadmin_user_edit')+'?uid='+str(obj.id)+'"</script>')
        
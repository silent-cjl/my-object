from django.shortcuts import render,reverse
from .. models import Types,Goods
from django.http import HttpResponse,JsonResponse
import os
# Create your views here.

def uploads(request):
    res = request.FILES.get('pics',None)
    print(res,type(res))
    if not res:
        return None
    endn = res.name.split('.').pop()
    import time,random
    pname = str(time.time())+str(random.randint(1,100000))+'.'+endn

    file = open('./static/goods/'+pname,'wb+')
    for chunk in res.chunks():
        file.write(chunk)
    file.close()
    return '/static/goods/'+pname



def add(request):
    if request.method=='GET':
        obj = Types.objects.extra(select={'path':'concat(path,id)'}).order_by('path')
        data = {'info':obj}
        
        return render(request,'myadmin/goods/add.html',data)
    
    else:
        try:
            data = request.POST.dict()
            print(data)
            del(data['csrfmiddlewaretoken'])
            # print(data['pid'],type(data['pid']))
            data['typeid']= Types.objects.get(id=int(data['typeid']))
            # del(data['pid'])
            s=uploads(request)
            data['pics'] = s
            print(data)

            obj = Goods.objects.create(**data)
            return HttpResponse('<script>alert("添加成功");location.href="'+reverse("myadmin_goods_list")+'"</script>')
        except:
            return HttpResponse('<script>alert("添加失败");location.href="'+reverse("myadmin_goods_add")+'"</script>')


def list(request):

    obj = Goods.objects.all()
    

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

    return render(request,'myadmin/goods/list.html',data)


def delete(request):

    try:
        uid = request.GET.get('uid',None)
        ob = Goods.objects.get(id=uid)

        

        ob.delete()  
        os.remove('.'+ob.pics)
        data = {'msg':'删除成功','code':0}
    except:
        data = {'msg':'删除失败','code':1}

    return JsonResponse(data)

def edit(request):
    id = request.GET.get('id',None)

    obj = Goods.objects.get(id=int(id))
    if request.method == 'GET':
        of = Types.objects.all()
        data = {'info':obj,'uinfo':of}

        return render(request,'myadmin/goods/edit.html',data)

    elif request.method == 'POST':

        try:
            if request.FILES.get('pics',None):
                # 判断是否使用的默认图
                if obj.pics:
                    print(obj.pics)
                    # 如果使用的不是默认图,则删除之前上传的头像
                    os.remove('.'+obj.pics)
                    
                # 执行上传
                obj.pics = uploads(request)
            obj.typeid= Types.objects.get(id=request.POST['typeid'])
            obj.title = request.POST['title']
            obj.descr = request.POST['descr']
            obj.price = request.POST['price']
            obj.store = request.POST['store']
            obj.status = request.POST['status']
            obj.save()
            return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myadmin_goods_list')+'"</script>')
        except:
            return HttpResponse('<script>alert("修改失败");location.href="'+reverse('myadmin_goods_edit')+'?id='+str(obj.id)+'"</script>')
        
    # return HttpResponse('3')

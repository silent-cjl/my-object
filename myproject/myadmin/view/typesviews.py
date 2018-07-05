from django.shortcuts import render,reverse
from .. models import Types
from django.http import HttpResponse,JsonResponse
# # Create your views here.
# def index(request):
#     return render(request,'myadmin/index.html')

def gettlist():
    tlist = Types.objects.extra(select={'path':'concat(path,id)'}).order_by('path')
    
    for i in tlist:
        if i.pid == 0:
            i.pname = '顶级分类'
        else:
            t = Types.objects.get(id=i.pid)
            i.pname = t.typename
        

    return tlist



def add(request):

    if request.method == 'GET':
        ob = gettlist

        return render(request,'myadmin/types/add.html',{'info':ob})

    elif request.method == 'POST':

        try:
            ob = Types()
            ob.typename = request.POST['typename']
            ob.pid = request.POST['pid']
            # print(ob.pid,type(ob.pid))
            if ob.pid == '0':
                ob.path = '0,'
            else:
                path = Types.objects.get(id=int(ob.pid)).path

                ob.path = path + ob.pid +','

            ob.save()

            return HttpResponse('<script>alert("添加成功");location.href="'+reverse("myadmin_types_list")+'"</script>')
        except: 
            return HttpResponse('<script>alert("添加失败");location.href="'+reverse("myadmin_types_add")+'"</script>')



def list(request):
    tlist = gettlist()

    #导入  django 分页模块
    from django.core.paginator import Paginator

    #实例化一个分页对象
    pages = Paginator(tlist,10)

    p = request.GET.get('p',1)

    typelist = pages.page(p)


    zpage = pages.num_pages

    data = {'uinfo':typelist,'num':zpage}
    return render(request,'myadmin/types/list.html',data)


def delete(request):
    try:
        uid = request.GET.get('uid',None)

        num = Types.objects.filter(pid=uid).count()
        if num != 0:
            data={'msg':'条件不符合要求，拒绝删除'}
        else:
            ob = Types.objects.get(id = uid)
            ob.delete()  
            data = {'msg':'删除成功','code':0}
    except:
        data = {'msg':'删除失败','code':1}

    return JsonResponse(data)

# def edit(request):

#     if request.method == "GET":

#         return render(request,'myadmin/types/edit.html')
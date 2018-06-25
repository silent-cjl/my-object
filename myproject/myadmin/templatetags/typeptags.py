from django import template
from django.utils.html import format_html

register = template.Library()

#自定义过滤器的装饰器
@register.simple_tag
def showpage(count,request):
    # print(count)
    endpage = count

    p = int(request.GET.get('p',1))
    if p < 5:
        if count > 10:
            count = 10
        start = 1
        end = count
    else:
        s = p+5
        if s > count:
            s = count
        start = s-9
        if start < 1:
            start = 1
        end = s

    res = ''
    for x in request.GET:
        if x != 'p':
            res += "&"+x+'='+request.GET[x]


    s = ''
    #首页
    if p ==1:
        s += '<li class="am-disabled"><a href="?p=1'+res+'">首页</a></li>'
    else:
        s += '<li class="am-active"><a href="?p=1'+res+'">首页</a></li>'
    #上一页
    if p ==1:
        s += '<li class="am-disabled"><a href="?p=1'+res+'">上一页</a></li>'
    else:
        s += '<li class="am-active"><a href="?p='+str(p-1)+res+'">上一页</a></li>'

    #页码
    for x in range(start,end+1):
        # print(x)
        if p == x:
            s += '<li class="am-active"><a href="?p='+str(x)+res+'">'+str(x)+'</a></li>'
        else:
            s += '<li><a href="?p='+str(x)+res+'">'+str(x)+'</a></li>'

    #下一页
    if p ==count:
        s += '<li class="am-disabled"><a href="?p=1'+res+'">下一页</a></li>'
    else:
        s += '<li class="am-active"><a href="?p='+str(p+1)+res+'">下一页</a></li>'

    #尾页
    if p == count:
        s += '<li class="am-disabled"><a href="?p='+str(endpage)+res+'">尾页</a></li>'
    else:
        s += '<li class="am-active"><a href="?p='+str(endpage)+res+'">尾页</a></li>'


    return format_html(s)

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from blog.models import Article, Category, Banner, Tag, Link

def hello(request):
    return HttpResponse("welcom my blog")

#首页
def index(request):
    allcategory = Category.objects.all()  # 通过Category表查出所有分类
    banner = Banner.objects.filter(is_active=True)[0:4]  # 通过filrter查询出所有激活的is_active幻灯图数据，并进行切片，只显示4条数据
    tui = Article.objects.filter(tui__id=1)[:3]  # 查询推荐位ID为1的文章
    allarticle = Article.objects.all().order_by('-id')[0:10]  #首页最新文章实现,最多显示10篇
    # 热门文章排行推荐
    #hot = Article.objects.all().order_by('?')[:10]#随机推荐
    #hot = Article.objects.filter(tui__id=3)[:10]   #通过推荐进行查询，以推荐ID是3为例
    hot = Article.objects.all().order_by('views')[:10]#通过浏览数进行排序
    tags = Tag.objects.all()  #右侧所有标签
    remen = Article.objects.filter(tui__id=2)[:6] #右侧热门推荐实现，通过后台推荐位为2来实现
    link = Link.objects.all()  #尾部友情链接
    # 把查询出来的分类封装到上下文里
    context = {
        'allcategory': allcategory,
        'banner': banner,  # 把查询到的幻灯图数据封装到上下文
        'tui': tui,
        'allarticle': allarticle,
        'hot': hot,
        'remen': remen,
        'tags': tags,
        'link': link,
    }
    return render(request, 'index.html', context)  # 把上下文传到index.html页面

#文章列表页
def list(request,lid):
    list = Article.objects.filter(category_id=lid)  # 获取通过URL传进来的lid，然后筛选出对应文章
    cname = Category.objects.get(id=lid)  # 获取当前文章的栏目名
    remen = Article.objects.filter(tui__id=2)[:6]  # 右侧的热门推荐
    allcategory = Category.objects.all()  # 导航所有分类
    tags = Tag.objects.all()  # 右侧所有文章标签
    page = request.GET.get('page')#在URL中获取当前页面数
    # 47-53使用的是Django自带一个强大的分页功能插件，从视图里导入使用
    paginator = Paginator(list, 5)#对查询到的数据对象list进行分页，设置超过5条数据就分页
    try:
        list = paginator.page(page)#获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)#如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)#如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

    return render(request, 'list.html', locals())

#内容页， 文章内容的URL是：网站域名/show-文章ID.html，文章ID是通过URL里的sid传进来的。
def show(request,sid):
    show = Article.objects.get(id=sid) #查询指定id的文章
    allcategory = Category.objects.all() #导航上的分类
    tags = Tag.objects.all() #右侧所有标签
    remen = Article.objects.filter(tui_id=2) #右侧热门推荐
    hot = Article.objects.all().order_by('?')[:10] #内容下面的你可能感兴趣的文章，随机推荐
    previous_blog = Article.objects.filter(created_time__gt=show.created_time,category=show.category.id).first()
    netx_blog = Article.objects.filter(created_time__lt=show.created_time,category=show.category.id).last()

    # 文章的浏览数，我们先通过show.views查询到当前浏览数，然后对这个数进行加1操作，意思是每访问一次页面（视图函数），
    # 就进行加1操作。然后再通过show.save()进行保存。
    show.views = show.views + 1
    show.save()
    return render(request, 'show.html', locals())

#标签页
def tag(request, tag):
    list = Article.objects.filter(tags__name=tag)#通过文章标签进行查询文章
    remen = Article.objects.filter(tui__id=2)[:6]
    allcategory = Category.objects.all()
    tname = Tag.objects.get(name=tag)#获取当前搜索的标签名
    page = request.GET.get('page')
    tags = Tag.objects.all()
    paginator = Paginator(list, 5)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'tags.html', locals())


# 搜索页
def search(request):
    ss=request.GET.get('search')#获取搜索的关键词
    list = Article.objects.filter(title__icontains=ss)#获取到搜索关键词通过标题进行匹配
    remen = Article.objects.filter(tui__id=2)[:6]
    allcategory = Category.objects.all()
    page = request.GET.get('page')
    tags = Tag.objects.all()
    paginator = Paginator(list, 10)
    try:
        list = paginator.page(page) # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1) # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages) # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'search.html', locals())


# 关于我们
def about(request):
    allcategory = Category.objects.all()
    return render(request, 'page.html',locals())


from django.contrib import admin
# Register your models here.
from blog.models import Article, Banner, Category, Tag, Tui, Link


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'tui', 'user', 'views', 'created_time')
    # 文章列表里显示想要的字段
    list_per_page = 50
    # 满50条数据就自动分页
    ordering = ('created_time',)
    # 后台数据排序方式
    list_display_links = ('id', 'title')
    # 设置哪些字段可以点进编辑界面

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_info', 'img', 'link_url', 'is_active')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'index')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Tui)
class TuiAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id','name','linkurl')


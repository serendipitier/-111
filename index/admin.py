from django.contrib import admin
from .models import *

# 修改title和header
admin.site.site_title = '电子公文传输系统后台管理系统'
admin.site.site_header = '电子公文传输系统'


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的列名设置
    list_display = ['id', 'name']
    # 设置可搜索的字段并在Admin后台数据生成搜索框
    # 如有外键应使用双下划线连接两个模型的字段
    search_fields = ['name']
    # 设置排序方式
    ordering = ['id']


@admin.register(Document)
class DoucmentAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的列名设置
    list_display = ['id', 'name', 'person', 'office', 'time', 'img', 'file', 'type', 'lyrics']
    # 设置可搜索的字段并在Admin后台数据生成搜索框
    # 如有外键应使用双下划线连接两个模型的字段
    search_fields = ['name', 'person', 'office']
    # 设置过滤器，在后台数据的右侧生成导航栏
    # 如有外键应使用双下划线连接两个模型的字段
    list_filter = ['office', 'type']
    date_hierarchy = 'time'
    # 设置排序方式
    ordering = ['id']


@admin.register(Dynamic)
class DynamicAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的列名设置
    list_display = ['id', 'document', 'plays', 'search', 'download']
    # 设置可搜索的字段并在Admin后台数据生成搜索框
    # 如有外键应使用双下划线连接两个模型的字段
    search_fields = ['document']
    # 设置过滤器，在后台数据的右侧生成导航栏
    # 如有外键应使用双下划线连接两个模型的字段
    list_filter = ['plays', 'search', 'download']
    # 设置排序方式
    ordering = ['id']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的列名设置
    list_display = ['id', 'text', 'user', 'document', 'date']
    # 设置可搜索的字段并在Admin后台数据生成搜索框
    # 如有外键应使用双下划线连接两个模型的字段
    search_fields = ['user', 'document', 'date']
    # 设置过滤器，在后台数据的右侧生成导航栏
    # 如有外键应使用双下划线连接两个模型的字段
    list_filter = ['text']
    date_hierarchy = 'date'
    # 设置排序方式
    ordering = ['id']


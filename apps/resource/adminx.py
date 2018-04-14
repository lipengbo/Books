# _*_ coding: utf-8 _*_
import xadmin

__author__ = "zero"
__data__ = "2018/4/12 18:46"
from .models import *


class YearBookAdmin(object):
    list_display = ['year', 'title', "category", 'identify', 'page']
    list_fileds = ['year']
    ordering = ['-year', 'identify']


xadmin.site.register(YearBook, YearBookAdmin)


class YearBookContentAdmin(object):
    list_display = ['year', 'content', "index"]
    list_fileds = ['year']
    ordering = ['-year', 'index']


xadmin.site.register(YearBookContent, YearBookContentAdmin)


class YearBookContentInline(object):
    model = YearBookContent
    extra = 0


class YearBookDesAdmin(object):
    list_display = ['year', 'chinese', 'pubtime', 'page', 'author']
    list_fileds = ['year']
    ordering = ['-year']
    inlines = [YearBookContentInline]


xadmin.site.register(YearBookDes, YearBookDesAdmin)
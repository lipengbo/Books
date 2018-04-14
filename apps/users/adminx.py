#!/usr/bin/env python
# encoding: utf-8

import xadmin
from xadmin import views
from .models import PhoneCode, EmailCode, ImageCode


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # site_title = "农村统计年鉴后台管理系统"
    site_footer = "agristatics"
    # menu_style = "accordion"


class PhoneCodeAdmin(object):
    list_display = ['code', 'mobile', "add_time"]
    ordering = ['-add_time']


class EmailCodeAdmin(object):
    list_display = ['code', 'email', "add_time"]
    ordering = ['-add_time']


class ImageCodeAdmin(object):
    list_display = ['code', 'image', "add_time"]
    ordering = ['-add_time']


xadmin.site.register(PhoneCode, PhoneCodeAdmin)
xadmin.site.register(EmailCode, EmailCodeAdmin)
xadmin.site.register(ImageCode, ImageCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

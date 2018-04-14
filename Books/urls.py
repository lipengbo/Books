"""Books path Configuration

The `pathpatterns` list routes paths to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/paths/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a path to pathpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a path to pathpatterns:  path('', Home.as_view(), name='home')
Including another pathconf
    1. Import the include() function: from django.paths import include, path
    2. Add a path to pathpatterns:  path('blog/', include('blog.paths'))
"""
# from django.contrib import admin
import xadmin
from django.conf.urls.static import static

from django.urls import include, path, re_path
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from Books import settings
from Books.settings import MEDIA_ROOT
# from Books.settings import STATIC_ROOT
from resource.views import ResourceView

# 验证用户
from apps.users.views import *

router = DefaultRouter()
router.register("users", UserViewset, base_name='users')
router = DefaultRouter()

# 配置手机验证码url
router.register("phonecodes", PhoneCodeViewset, base_name='phonecodes')

# 配置邮箱验证码url
router.register("emailcodes", EmailCodeViewset, base_name='emailcodes')

# 验证用户
router.register("users", UserViewset, base_name='users')

# 验证图片验证码
router.register('verify', ImageCodeVerifyViewset, base_name='verify')


urlpatterns = [
    path('admin/', xadmin.site.urls),
    path('', ResourceView.as_view(), name='years'),
    path('years/', ResourceView.as_view(), name='years'),
    #  数据列表页
    re_path(r'^', include(router.urls)),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # re_path(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    # jwt认证模式
    path(r'api-token-auth/', obtain_jwt_token),
    path(r'access/', obtain_jwt_token),

    # 用户登录注册页面
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('forget/', ForgetView.as_view(), name="forget"),
    path(r'account/', AccountView.as_view(), name='account'),
    path(r'active/', ActivateViewset.as_view(), name='active'),
    path(r'personal/', PersonalViewset.as_view(), name='personal'),
    path(r'captcha/', include('captcha.urls')),

]

# 全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'

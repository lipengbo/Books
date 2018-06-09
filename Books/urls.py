import xadmin

from django.urls import include, path, re_path
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from Books.settings import MEDIA_ROOT
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
    path(r'^', include(router.urls)),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # re_path(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    # jwt认证模式
    path(r'api-token-auth/', obtain_jwt_token),
    path(r'access/', obtain_jwt_token),

    # 用户登录注册页面
    re_path('^user/', include('users.urls')),

    path(r'captcha/', include('captcha.urls')),

]

# 全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'

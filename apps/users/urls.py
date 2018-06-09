from django.urls import re_path

from .views import *



urlpatterns = [
    re_path('^logout/$', LogoutView.as_view(), name="logout"),
    re_path('^register/$', RegisterView.as_view(), name="register"),
    re_path('^login/$', LoginView.as_view(), name="login"),
    re_path('^forget/$', ForgetView.as_view(), name="forget"),
    re_path(r'^personal/$', PersonalViewset.as_view(), name='personal'),
    re_path(r'^account/$', AccountView.as_view(), name='account'),
]
from django.urls import path

from .views import *



urlpatterns = [
    path('logout', LogoutView.as_view(), name="logout"),
    path('register', RegisterView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('forget', ForgetView.as_view(), name="forget"),
    path(r'personal', PersonalViewset.as_view(), name='personal'),
    path(r'account', AccountView.as_view(), name='account'),
]
from random import choice, Random

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout
from django.urls import reverse
from django.views import View
from rest_framework import viewsets, status, mixins, authentication, permissions
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.utils import jwt_encode_handler

from Books.settings import YUN_KEY
from tools.codes import send_email, SmsPhoneCode
from users.forms import RegisterForm
from users.serializers import *
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

User = get_user_model()


class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if User.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            pass_word = request.POST.get("password", "")
            user_profile = User()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_email(user_name, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


class LoginView(View):
    def get(self, request):
        login_form = RegisterForm()
        return render(request, "login.html", {'register_form': login_form})

    # def post(self, request):
    #     login_form = LoginForm(request.POST)
    #     if login_form.is_valid():
    #         user_name = request.POST.get("email", "")
    #         pass_word = request.POST.get("password", "")
    #         user = authenticate(username=user_name, password=pass_word)
    #         if user is not None:
    #             if user.is_active:
    #                 login(request, user)
    #                 return HttpResponseRedirect(reverse("years"))
    #             else:
    #                 return render(request, "login.html", {"msg": "用户未激活！"})
    #         else:
    #             return render(request, "login.html", {"msg": "用户名或密码错误！"})
    #     else:
    #         return render(request, "login.html", {"login_form": login_form})


class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        response = HttpResponseRedirect(reverse("years"))
        response.set_cookie(key="name", expires=datetime.now() - timedelta(days=1))
        response.set_cookie(key="token", expires=datetime.now() - timedelta(days=1))
        return response


class PersonalViewset(View):
    def get(self, request):
        return render(request, "personal.html")


class ForgetView(View):
    def get(self, request):
        return render(request, "forgetpwd.html")


class AccountView(View):
    def get(self, request):
        return render(request, "account.html")


class ActivateViewset(View):
    def get(self, request):
        email = request.GET.get("email", "")
        code = request.GET.get('code', "")

        if EmailCode.objects.filter(email=email, code=code).exists():
            result = User.objects.filter(Q(username=email) | Q(email=email))
            result[0].is_active = True
            result[0].save()
        return render(request, "login.html")


class PhoneCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送手机验证码
    """
    serializer_class = PhoneSerialier

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # drf可以捕做捉异常返回400
        code = self.generate_code()

        mobile = serializer.validated_data['mobile']

        yun_pian = SmsPhoneCode(YUN_KEY)

        sms_status = yun_pian.send_msg(code=code, mobile=mobile)
        if sms_status['code'] != 0:
            return Response({
                "mobile": sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = PhoneCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                'mobile': mobile
            }, status=status.HTTP_201_CREATED)


class EmailCodeViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送邮箱验证码
    """

    def get_queryset(self):
        queryset = ''
        if self.action == 'retrieve':
            queryset = User.objects.all()
        elif self.action == 'create':
            queryset = EmailCode.objects.all()
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    def generate_code(self, ranglength=4):
        str = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(ranglength):
            str += chars[random.randint(0, length)]
        return str

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserExitSerialier
        elif self.action == 'create':
            return EmailSerialier
        elif self.action == 'list':
            return EmailVerifySerialier
        return EmailSerialier


    # 验证邮箱是否存在
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        return Response(email, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # drf可以捕做捉异常返回400
        send_type = serializer.validated_data['send_type']
        email = serializer.validated_data['email']
        if send_type == 'activate':
            code = self.generate_code(16)
        else:
            code = self.generate_code(4)
        sms_status = send_email(code=code.lower(), email=email, send_type=send_type)
        if not sms_status:
            return Response({
                "msg": '邮件发送失败，请重新发送！'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = EmailCode(code=code.lower(), email=email, send_type=send_type)
            code_record.save()
            return Response({
                'msg': '邮件发送成功，请注意查收！'
            }, status=status.HTTP_201_CREATED)

    # 验证邮箱验证码是否正确 get
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        response = Response(email, status=status.HTTP_200_OK)
        if email:
            if serializer.validated_data['send_type'] == 'register':

                response = Response(True, status=status.HTTP_200_OK)

            elif serializer.validated_data['send_type'] == 'forget':

                user = User.objects.get(Q(username=email) | Q(email=email))
                payload = jwt_payload_handler(user)
                re_dict = serializer.data
                re_dict['token'] = jwt_encode_handler(payload)
                headers = self.get_success_headers(re_dict)
                headers['Authorization'] = "token " + re_dict['token']
                response = Response(True, status=status.HTTP_200_OK, headers=headers)
                expires = datetime.now() + timedelta(days=1)
                response.set_cookie('token', re_dict['token'], expires=expires)
                response.set_cookie('name', re_dict['username'], expires=expires)

        return response


class EmailCodeVereifyViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送邮箱验证码
    """
    serializer_class = EmailVerifySerialier

    queryset = EmailCode.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['verify']
        send_type = serializer.validated_data['send_type']
        data = False
        statuscode = status.HTTP_200_OK
        exit = EmailCode.objects.filter(code=str(code).lower(), email=email, send_type=send_type)
        if exit:
            data = True
        return Response(data, status=statuscode)


class ImageCodeVerifyViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    验证图片验证码
    """
    serializer_class = ImageCodeVerifySerialier
    queryset = EmailCode.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.validated_data['response']
        hashkey = serializer.validated_data['hashkey']
        data = False
        statuscode = status.HTTP_200_OK
        exit = CaptchaStore.objects.filter(response=str(response).lower(), hashkey=hashkey)
        if exit:
            data = True
        return Response(data, status=statuscode)


class UserViewset(CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    # serializer_class = UserRegSerializer
    queryset = User.objects.all()
    # permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (authentication.SessionAuthentication, JSONWebTokenAuthentication)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated(), ]
        elif self.action == 'create':
            return []
        return []

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer

        return UserDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        headers = self.get_success_headers(re_dict)
        headers['Authorization'] = "token " + re_dict['token']
        re_dict['name'] = user.name if user.first_name else user.username
        response = Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)
        response.set_cookie("name", re_dict['name'], expires=datetime.now() + timedelta(days=1))
        response.set_cookie("token", re_dict['token'], expires=datetime.now() + timedelta(days=1))
        return response

    # 重载获取用户model的实例
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response



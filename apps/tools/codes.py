# _*_ coding: utf-8 _*_
import json

import requests
from django.core.mail import send_mail

from Books.settings import HOST, EMAIL_FROM


class SmsPhoneCode(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_msg(self, code, mobile):
        parmas = {
            'apikey': self.api_key,
            "mobile": mobile,
            "text": "【农业统计数据】您的验证码是{}".format(code)
        }
        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        return re_dict


def send_email(email, code, send_type="register"):
    data = False
    title = "【农业统计年鉴】"
    email_body = """<table width="500" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff" 
    align="center"><tbody> <td><table width="500" height="40" cellspacing="0" cellpadding="0" border="0" 
    align="center"></table></td> <tr> <td> <table width="500" height="48" cellspacing="0" cellpadding="0" border="0" 
    bgcolor="#10A64F" backgroud-color='transparent' align="center"> <tbody> <tr> <td border="0" 
    style="padding-left:20px;" width="74" valign="middle" height="26" align="center"> <a href="{host}/index" 
    target="_blank"><img src="{host}/static/img/chartsite.png" width="176" height="36" border="0"> </a> </td> 
    <td colspan="2" style="color:#ffffff; padding-right:20px;"width="500" valign="middle" height="48" align="right"> 
    <a href="{host}/index" target="_blank" style="color:#ffffff;text-decoration:none;font-size:16px"> 首页</a> </td> 
    </tr> </tbody></table> </td> </tr> <tr> <td> <table style="border:1px solid 
    #edecec;border-top:none;border-bottom:none;padding:0 20px;font-size:14px;color:#333333;" width="500" 
    cellspacing="0" cellpadding="0" border="0" align="left"> <tbody> <tr> <td border="0" colspan="2" style=" 
    font-size:16px;vertical-align:bottom;" width="500" height="56" align="left">尊敬的用户：</a></td> </tr> <tr> <td 
    border="0" style="padding-left:40px;font-size:12px;"width="360" height="32">{email}, 您好</td></tr> <tr> <td 
    border="0" style="padding-left:40px;font-size:12px;"width="360" height="32">欢迎加入农业统计年鉴，请妥善保管您的验证信息：</td> </tr> 
    <tr> <td colspan="2" style="padding-left:40px;font-size:12px;" width="360" height="32">{notice}<br><a href="{url}" 
    style="text-decoration:none" target="_blank">{url}</a> </td> </tr><tr><td colspan="2" style="line-height:30px; 
    border-bottom:1px  dashed #e5e5e5;font-size:12px;text-align: left;padding-left: 320px;" width="360" height="14"> 
    农业统计年鉴</td></tr><tr><td colspan="2" style="padding:8px0 28px;color:#999999; font-size:12px;text-align: right; 
    padding-right: 40px;" width="360" height="14">此为系统邮件请勿回复</td></tr></tbody></table></td></tr><td><table 
    width="500" height="40" cellspacing="0" cellpadding="0" border="0" align="center"></table></td></tbody></table> """

    if send_type == "activate":
        email_title = title + "账号激活链接"
        url = '{host}/active?email={email}&code={email}'.format(host=HOST, email=email, code=code)
        email_body = email_body.format(host=HOST, notice="请点击下面的链接激活你的账号(此链接有效期为24小时):", url=url, email=email)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email], html_message=email_body)
        if send_status:
            data = True
        return data
    elif send_type == 'invited':
        email_title = title + "邀请邮件"
        email_body = email_body.format(host=HOST,
                                       notice=code,
                                       url='快来加入吧！',
                                       email=email).replace("欢迎加入农业统计年鉴，请妥善保管您的验证信息：", '您的好友通过农业统计年鉴可视化平台向你发出邀请：')
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email], html_message=email_body)
        if send_status:
            data = True
        return data
    else:
        email_title = "邮箱验证码"
        email_body = title + "你的邮箱验证码为: {0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            data = True
        return data

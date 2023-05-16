import json

import django_redis
from AgentLogin import AgentLogin
from django.conf import settings
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View


# qq登陆接口1：获取扫码页面url
from oauth.models import QQUser

from user.models import UserModel
from QTribe.utils.bind import generate_secret_openid, check_secret_openid


class GetQQUrl(View):
    def get(self, request):
        # 获得QQ扫码的链接地址
        qq_url = AgentLogin.qq_url(settings.QQ_CLIENT_ID, settings.QQ_REDIRECT_URI)

        return JsonResponse({'code': '200', 'login_url': qq_url})


class BindQQ(View):
    def get(self, request):
        # 捕获参数code
        code = request.GET.get('code')
        # 获取openid
        userinfo, openid = AgentLogin.qq(settings.QQ_CLIENT_ID, settings.QQ_APP_KEY, settings.QQ_REDIRECT_URI, code)
        print('openid------>',openid)
        # 根据openid判断用户是否已经绑定
        user = QQUser.objects.filter(openid=openid)
        # 若已绑定，就直接进入新闻页面
        if user:
            return redirect('/index/home_index/')
        # 若没有绑定，就进入绑定页面
        sec_openid = generate_secret_openid(openid)  # 加密
        print('generate------>',sec_openid)
        return render(request, 'oauth/bind_qq.html', {'sec_openid': sec_openid})
    def post(self,request):
        data=json.loads(request.body)

        phone=data.get('phone')
        smscode=data.get('smscode')
        password=data.get('password')
        sec_openid=data.get('sec_openid')
        user=UserModel.objects.get(phone=phone)
        print('password---->',password)
        print('sec_openid---->',sec_openid)
        if not user:
            return JsonResponse({'code':4001,'errormsg':'该手机号未绑定用户，请先注册'})
        redis_conn=django_redis.get_redis_connection('verify_code')
        code_rel=redis_conn.get(f'sms{phone}').decode('utf-8')
        if code_rel!=smscode:
            return JsonResponse({'code':4002,'errormsg':'验证码输入错误'})
        if not user.check_password(password):
            return JsonResponse({'code': 4003, 'errormsg': '密码错误'})

        openid = check_secret_openid(sec_openid)
        QQUser.objects.create(user=user,openid=openid)
        login(request,user)
        return JsonResponse({'code': 200})




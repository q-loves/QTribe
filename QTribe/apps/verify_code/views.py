import random
import string

import django_redis
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from QTribe.utils.smscode import send_sms_code


class SendSmsCode(View):
    def get(self,request,phone):
        #生成验证码
        num=string.digits
        num_list=random.choices(num,k=6)
        code=''.join(num_list)
        #将code保存到redis数据库中
        redis_conn=django_redis.get_redis_connection('verify_code')
        redis_conn.setex(f'sms{phone}',60,code)
        # ret=send_sms_code(code, phone)
        ret={'code':2}
        if ret.get('code')==2:
            return JsonResponse({'code':'200','errormsg':'ok'})
        return JsonResponse({'code':'5001','errormsg':'短信发送错误'})

class CheckSmsCode(View):
    def get(self,request,phone):
        #接收参数
        code=request.GET.get('smscode')
        if not all([phone,code]):
            return JsonResponse({'code':'4001'})
        #将该电话号码对应的验证码从数据库中提取出来
        redis_conn=django_redis.get_redis_connection('verify_code')
        code_real=redis_conn.get(f'sms{phone}').decode('utf-8')
        if code_real is None:
            return JsonResponse({'code':'4002','errormsg':'验证码已过期'})
        if code_real!=code:
            return JsonResponse({'code':'4003','errormsg':'验证码错误'})
        return JsonResponse({'code':'200','errormsg':'ok'})

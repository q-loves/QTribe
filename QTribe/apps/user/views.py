import json

from django.contrib import auth
from django.contrib.admin import action
from django.db.models import F
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from user.models import UserModel




class Register(View):

    def get(self,request):
        return render(request,'user/register.html')
    def post(self,request):
        state={'code':-1}
        username=request.POST.get('username')
        password=request.POST.get('password')
        phone=request.POST.get('phone')
        user=UserModel.objects.create_user(username=username,password=password,phone=phone)
        if user:
            state={'code':200}
            auth.login(request,user)
        return redirect('/index/home_index/')
#校验用户名
class CheckUsername(View):
    def get(self,request,username):
        count=UserModel.objects.filter(username=username).count()
        return JsonResponse({'count':count})
#校验电话号码
class CheckPhone(View):
    def get(self,request,phone):
        count=UserModel.objects.filter(phone=phone).count()
        return JsonResponse({'count':count})

#校验邮箱地址
class CheckEmail(View):
    def get(self,request,email):
        count=UserModel.objects.filter(email=email).count()
        return JsonResponse({'count':count})

#校验密码
class ResetPassword(View):
    def get(self,request):
        password=request.GET.get('password')

        if request.user.check_password(password):
            return JsonResponse({'code':200})
        return JsonResponse({'code':401})
    def post(self,request):
        try:
            data=json.loads(request.body)
            password=data['password']
            request.user.set_password(password)
            return JsonResponse({'code':200})
        except:
            return JsonResponse({'code':401})



class Login(View):
    def get(self,request):
        return render(request,'user/login.html')
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)
        if user:
            auth.login(request,user)
            return redirect('/index/home_index/')
        return HttpResponse('用户名或密码错误')

class Transform(View):
    def get(self,request):
        type=request.GET.get('type')
        if type=='register':
            return render(request, 'user/login.html')
        if type=='login':
            return render(request, 'user/register.html')
        return render(request,'404.html')

class UpdateInformation(View):
    def get(self,request):
        return render(request,'user/update_information.html',{'user':request.user})
    def post(self,request):

        try:
            data=json.loads(request.body)
            #利用新字典接收不为空的数据
            dict={}
            for key in data:
                if data.get(key):
                    dict[key]=data.get(key)
            user=UserModel.objects.filter(id=request.user.id).update(**dict)
            return JsonResponse({'code':200})
        except:
            return JsonResponse({'code':401})



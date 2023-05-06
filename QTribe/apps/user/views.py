from django.contrib.admin import action
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from user.models import UserModel

#注册
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
        return JsonResponse(state)
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


class Login(View):

    def get(self,request):
        return render(request,'login.html')
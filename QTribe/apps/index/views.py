from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View

#平台介绍页面


class HomePage(View):
    def get(self,request):
        return render(request,'base.html',{'user':request.user})

#404页面
class NoFindPage(View):
    def get(self,request):
        return render(request,'404.html')


#查看个人资料
class Information(View):
    def get(self,request):

        return render(request,'pieces/information.html',{'user':request.user})


from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View

#平台介绍页面
from region.models import Nation, Province, City


class HomePage(View):
    def get(self,request):
        return render(request,'base.html',{'user':request.user})

#404页面
class NoFindPage(View):
    def get(self,request):
        return render(request,'404.html')

#上传文章
class PublishArticle(View):
    def get(self,request):
        return render(request,'pieces/publish_article.html')

#查看个人资料
class Information(View):
    def get(self,request):
        nation=Nation.objects.get(id=request.user.nation_id)
        province=Province.objects.get(id=request.user.province_id)
        city=City.objects.get(id=request.user.city_id)
        return render(request,'pieces/information.html',{'user':request.user,'nation':nation,'province':province,'city':city})




from django.db.models import F
from django.shortcuts import render
from django.views import View

#自己的生活列表页面
class MyLife(View):
    def get(self,request):
        return render(request,'pieces/my_life.html')

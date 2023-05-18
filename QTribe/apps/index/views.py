from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View

#平台介绍页面
from pieces_info.models import VideoModel, ArticleModel


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

class VideoMall(View):
    def get(self,request):
        page_number = int(request.GET.get('page_number', 1))
        # 获取该平台所有视频
        star_ids=[]#用于筛选用户点赞过的视频，方便前端渲染
        video_list = VideoModel.objects.all()
        for video in video_list:
            objs=request.user.starmodel_set.all()
            for obj in objs:
                if obj.video==video:
                    star_ids.append(video.id)

        # 创建分页对象
        paginator = Paginator(video_list, 2)
        num_pages = paginator.num_pages
        # 获取页码数列，用于前端遍历
        if paginator.num_pages > 5:
            if page_number - 2 <= 1:
                page_list = range(1, 6)
            elif page_number + 2 >= num_pages:
                page_list = range(num_pages - 4, num_pages + 1)
            else:
                page_list = range(page_number - 1, page_number + 4)

        else:
            page_list = paginator.page_range
        try:
            # 获取对应页数的全部视频
            page_content = paginator.page(page_number)
        except PageNotAnInteger:
            page_content = paginator.page(1)
        except EmptyPage:
            page_content = paginator.page(num_pages)
        return render(request, 'public/video_mall.html', {'page_content': page_content,
                                                        'page_list': page_list,
                                                        'current_page': page_content.number,
                                                        'num_pages': num_pages,
                                                        'star_ids':star_ids})
#文章列表页面
class ArticleMall(View):
    def get(self,request):
        page_number = int(request.GET.get('page_number', 1))
        articles=ArticleModel.objects.all()
        star_ids=[]#用于筛选用户点赞过的视频，方便前端渲染
        for article in articles:
            objs=request.user.starmodel_set.all()
            for obj in objs:
                if obj.article==article:
                    star_ids.append(article.id)
        # 创建分页对象
        paginator = Paginator(articles, 2)
        num_pages = paginator.num_pages
        # 获取页码数列，用于前端遍历
        if paginator.num_pages > 5:
            if page_number - 2 <= 1:
                page_list = range(1, 6)
            elif page_number + 2 >= num_pages:
                page_list = range(num_pages - 4, num_pages + 1)
            else:
                page_list = range(page_number - 1, page_number + 4)

        else:
            page_list = paginator.page_range
        try:
            # 获取对应页数的全部视频
            page_content = paginator.page(page_number)
        except PageNotAnInteger:
            page_content = paginator.page(1)
        except EmptyPage:
            page_content = paginator.page(num_pages)
        return render(request, 'public/article_mall.html', {'page_content': page_content,
                                                        'page_list': page_list,
                                                        'current_page': page_content.number,
                                                        'num_pages': num_pages,
                                                        'star_ids':star_ids})

class LifeMall(View):
    def get(self,request):
        return render(request,'public/life_mall.html')
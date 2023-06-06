from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View

#平台介绍页面
from pieces_info.models import VideoModel, ArticleModel,LifeModel

from user.models import UserModel,FocusModel

class StartIt(View):
    def get(self,request):
        return render(request,'start/index.html')

class HomePage(View):
    def get(self,request):
        return render(request,'center2.html',{'user':request.user})

#404页面
class NoFindPage(View):
    def get(self,request):
        return render(request,'404.html')


#查看个人资料
class Information(View):
    def get(self,request):
        return render(request,'pieces/information.html',{'user':request.user})

#视频广场
class VideoMall(View):
    def get(self,request):

        page_number = int(request.GET.get('page_number', 1))
        # 获取该平台所有视频
        star_ids=[]#用于筛选用户点赞过的视频，方便前端渲染
        video_list = VideoModel.objects.all()
        for video in video_list:
            objs=request.user.starmodel_set.all()
            for obj in objs:
                if obj.video==video and obj.flag=='1':
                    star_ids.append(video.id)
        collection_ids=[]#用于筛选用户收藏过的视频，方便前端渲染
        for video in video_list:
            objs=request.user.collectionmodel_set.all()
            for obj in objs:
                if obj.video==video and obj.flag=='1':
                    collection_ids.append(video.id)

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
                                                        'star_ids':star_ids,
                                                        'collection_ids':collection_ids,})
#文章广场
class ArticleMall(View):
    def get(self,request):
        page_number = int(request.GET.get('page_number', 1))
        articles=ArticleModel.objects.all()
        star_ids=[]#用于筛选用户点赞过的视频，方便前端渲染
        for article in articles:
            objs=request.user.starmodel_set.all()
            for obj in objs:
                if obj.article==article and obj.flag=='1':
                    star_ids.append(article.id)
        collection_ids=[]#用于筛选用户收藏过的视频，方便前端渲染
        for article in articles:
            objs=request.user.collectionmodel_set.all()
            for obj in objs:
                if obj.article==article and obj.flag=='1':
                    collection_ids.append(article.id)
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
                                                        'star_ids':star_ids,
                                                        'collection_ids':collection_ids,
                                                        })

class LifeMall(View):
    def get(self,request):
        page_number = int(request.GET.get('page_number', 1))
        lives=LifeModel.objects.all()
        star_ids=[]#用于筛选用户点赞过的视频，方便前端渲染
        for life in lives:
            objs=request.user.starmodel_set.all()
            for obj in objs:
                if obj.life==life and obj.flag=='1':
                    star_ids.append(life.id)
        collection_ids=[]#用于筛选用户收藏过的视频，方便前端渲染
        for life in lives:
            objs=request.user.collectionmodel_set.all()
            for obj in objs:
                if obj.life==life and obj.flag=='1':
                    collection_ids.append(life.id)

        # 创建分页对象
        paginator = Paginator(lives, 2)
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
        return render(request, 'public/life_mall.html', {'page_content': page_content,
                                                        'page_list': page_list,
                                                        'current_page': page_content.number,
                                                        'num_pages': num_pages,
                                                        'star_ids':star_ids,
                                                        'collection_ids':collection_ids,
                                                        })

#其他用户
class OtherUser(View):
    def get(self,request):
        page_number = int(request.GET.get('page_number', 1))
        users=UserModel.objects.exclude(id=request.user.id).all()
        objs=request.user.focusmodel_set.all()
        focus_ids=[]#查询用户关注的用户
        icon_ids=[]
        for obj in objs:
            if obj.flag=='1':
                focus_ids.append(obj.focus_user_id)
        for user in users:
            if  user.icon:
                icon_ids.append(user.id)
        # 创建分页对象
        paginator = Paginator(users, 10)
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
        return render(request, 'user/other_user.html', {'page_content': page_content,
                                                        'page_list': page_list,
                                                        'current_page': page_content.number,
                                                        'num_pages': num_pages,
                                                        'focus_ids':focus_ids,
                                                        'icon_ids':icon_ids,})
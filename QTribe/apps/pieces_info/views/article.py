
#自己的文章列表页面
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.db.models import F
from pieces_info.models import ArticleModel,ImageModel

#上传文章
from user.models import StarModel


class PublishArticle(View):
       def get(self,request):
            return render(request,'pieces/publish_article.html')
       def post(self,request):
           title=request.POST.get('title')
           content=request.POST.get('content')
           image=request.FILES.get('image')
           try:
               with transaction.atomic():#数据库绑定事物
                   article=ArticleModel.objects.create(title=title,content=content,default_img=image,user=request.user)
                   ImageModel.objects.create(image=image,user=request.user,article=article)
                   return JsonResponse({'code': 200})
           except:
               return JsonResponse({'code': 401})
#文章列表页面
class MyArticle(View):
    def get(self,request):
        page_number = int(request.GET.get('page_number', 1))
        articles=ArticleModel.objects.filter(user=request.user)
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
        return render(request, 'pieces/my_article.html', {'page_content': page_content,
                                                        'page_list': page_list,
                                                        'current_page': page_content.number,
                                                        'num_pages': num_pages})


#文章点赞量
class StarArticle(View):
    def get(self,request):
        a_id=int(request.GET.get('a_id'))
        current_page=int(request.GET.get('current_page'))
        article = ArticleModel.objects.get(id=a_id)
        is_star=StarModel.objects.filter(user_id=request.user.id,article_id=a_id)
        if is_star:
            article.star_count-=1
            article.save()
            StarModel.objects.filter(user_id=request.user.id, article_id=a_id).delete()
            return redirect(f'/index/article_mall?page_number={current_page}')
        else:
            article.star_count+=1
            article.save()
            StarModel.objects.create(user=request.user,article=article)
            return redirect(f'/index/article_mall?page_number={current_page}')
#文章顶置
class TopArticle(View):
    def get(self,request):
        a_id=int(request.GET.get('a_id'))
        is_top=int(request.GET.get('is_top'))
        current_page = int(request.GET.get('current_page'))
        if is_top==1:
            ArticleModel.objects.filter(id=a_id).update(is_top=0)
            return redirect(f'/pieces/my_article/?page_number={current_page}')
        if is_top==0:
            ArticleModel.objects.filter(id=a_id).update(is_top=1)
            return redirect(f'/pieces/my_article/?page_number={current_page}')

#观看文章内容,增加浏览次数，并且打开文章内容页面
class DetailsArticle(View):
    def get(self,request):
        a_id=int(request.GET.get('a_id'))
        article=ArticleModel.objects.get(id=a_id)
        article.running_count+=1
        article.save()
        return render(request,'pieces/article_details.html',{'article':article})
#删除视频
class DeleteArticle(View):
    def get(self,request):
        a_id=int(request.GET.get('a_id'))
        current_page=int(request.GET.get('current_page'))
        ArticleModel.objects.filter(id=a_id).delete()
        try:
            return redirect(f'/pieces/my_article?page_number={current_page}')
        except:
            return redirect(f'/pieces/my_article?page_number={current_page-1}')
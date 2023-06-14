from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from haystack.query import EmptySearchQuerySet
from haystack.views import SearchView

from pieces_info.models import LifeModel

from pieces_info.models import ImageModel

from user.models import StarModel, CollectionModel

from QTribe.tasks import send_message


class ShareLife(View):
    def get(self,request):
        return render(request,'pieces/share_life.html')
    def post(self,request):
        try:
            copy=request.POST.get('copy')
            switch=request.POST.get('switch')
            status=request.POST.get('like')
            images=request.FILES.getlist('files')
            with transaction.atomic():
                life=LifeModel.objects.create(copy=copy,user=request.user)
                if switch=='on':
                    life.is_friend=1
                if images:
                    list=[]
                    life.default_img=images[0]
                    for image in images:
                        list.append(ImageModel(image=image,user=request.user,life=life))
                life.status=status
                life.save()
                #批量插入
                ImageModel.objects.bulk_create(list)
            return JsonResponse({'code':200})
        except:
            return JsonResponse({'code': 500})

#自己的生活列表页面
class MyLife(View):
    def get(self,request):
        page_number = int(request.GET.get('page_number', 1))
        lives=LifeModel.objects.filter(user=request.user)
        # 创建分页对象
        paginator = Paginator(lives, 5)
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
        return render(request, 'pieces/my_life.html', {'page_content': page_content,
                                                        'page_list': page_list,
                                                        'current_page': page_content.number,
                                                        'num_pages': num_pages})
#文章点赞量
class StarLife(View):
    def get(self,request):
        l_id=int(request.GET.get('l_id'))
        current_page=int(request.GET.get('current_page'))
        q = request.GET.get('q')
        args = request.GET.get('args')  # 判断是从看点广场页面进入，还是从点赞列表页面进入
        life = LifeModel.objects.get(id=l_id)
        try:
            is_star=StarModel.objects.get(user_id=request.user.id,life_id=l_id)
            flag=is_star.flag
        except:
            is_star=0
        if is_star and flag=='1':
            life.star_count-=1
            life.save()
            is_star.flag = '0'
            is_star.save()
            if args == 'mall':
                return redirect(f'/index/life_mall?page_number={current_page}')
            if args == 'star':  # 有可能用户取消点赞后，当页就没有内容，防止报错，加一个try
                try:
                    return redirect(f'/pieces/star_life_list?page_number={current_page}')
                except:
                    return redirect(f'/pieces/star_life_list?page_number={current_page - 1}')
            if args == 'collect':
                return redirect(f'/pieces/collect_life_list?page_number={current_page}')
            if args=='search':
                return redirect(f'/pieces/search_life/?page={current_page}&q={q}')
        else:
            life.star_count+=1
            life.save()
            data={'u_id':request.user.id,'type_2':'star_life','p_id':l_id}
            send_message.delay(data)
            if not is_star:
                StarModel.objects.create(user=request.user,life=life,flag='1')
            else:
                is_star.flag = '1'
                is_star.save()
            if args == 'mall':
                return redirect(f'/index/life_mall?page_number={current_page}')
            if args == 'collect':
                return redirect(f'/pieces/collect_life_list?page_number={current_page}')
            if args=='search':
                return redirect(f'/pieces/search_life/?page={current_page}&q={q}')

#文章收藏量
class CollectLife(View):
    def get(self,request):
        l_id=int(request.GET.get('l_id'))
        current_page=int(request.GET.get('current_page'))
        q = request.GET.get('q')
        args = request.GET.get('args')  # 判断是从看点广场页面进入，还是从收藏列表页面进入
        life = LifeModel.objects.get(id=l_id)
        try:
            is_collect=CollectionModel.objects.get(user_id=request.user.id,life_id=l_id)
            flag=is_collect.flag
        except:
            is_collect=0
        if is_collect and flag=='1':
            life.collection_count-=1
            life.save()
            is_collect.flag = '0'
            is_collect.save()
            if args == 'mall':
                return redirect(f'/index/life_mall?page_number={current_page}')
            if args == 'collect':
                try:
                    return redirect(f'/pieces/collect_life_list?page_number={current_page}')
                except:
                    return redirect(f'/pieces/collect_life_list?page_number={current_page - 1}')
            if args == 'star':
                return redirect(f'/pieces/star_life_list?page_number={current_page}')
            if args=='search':
                return redirect(f'/pieces/search_life/?page={current_page}&q={q}')
        else:
            life.collection_count+=1
            life.save()
            data={'u_id':request.user.id,'type_2':'collect_life','p_id':l_id}
            send_message.delay(data)
            if not is_collect:
                CollectionModel.objects.create(user=request.user,life=life,flag='1')
            else:
                is_collect.flag = '1'
                is_collect.save()
            if args == 'mall':
                return redirect(f'/index/life_mall?page_number={current_page}')
            if args == 'star':
                return redirect(f'/pieces/star_life_list?page_number={current_page}')
            if args=='search':
                return redirect(f'/pieces/search_life/?page={current_page}&q={q}')

#文章顶置
class TopLife(View):
    def get(self,request):
        l_id=int(request.GET.get('l_id'))
        is_top=int(request.GET.get('is_top'))
        current_page = int(request.GET.get('current_page'))
        if is_top==1:
            LifeModel.objects.filter(id=l_id).update(is_top=0)
            return redirect(f'/pieces/my_life/?page_number={current_page}')
        if is_top==0:
            LifeModel.objects.filter(id=l_id).update(is_top=1)
            return redirect(f'/pieces/my_life/?page_number={current_page}')

#观看文章内容,增加浏览次数，并且打开文章内容页面
class DetailsLife(View):
    def get(self,request):
        l_id=int(request.GET.get('l_id'))
        life=LifeModel.objects.get(id=l_id)
        life.running_count+=1
        life.save()
        images=life.image.all()
        imgs=[]
        for obj in images:
            imgs.append(obj.image)
        comments=life.comment.all()
        comms=[]
        for comment in comments:
            comms.append(comment)
        return render(request,'pieces/life_details.html',{'life':life,'imgs':imgs,'l_id':l_id,'comms':comms})
#删除文章
class DeleteLife(View):
    def get(self,request):
        l_id=int(request.GET.get('l_id'))
        current_page=int(request.GET.get('current_page'))
        LifeModel.objects.filter(id=l_id).delete()
        try:
            return redirect(f'/pieces/my_life?page_number={current_page}')
        except:
            return redirect(f'/pieces/my_life?page_number={current_page-1}')

#点赞文章列表页面
class StarLifeList(View):
    def get(self,request):
        page_number = int(request.GET.get('page_number', 1))
        star_ids=[]
        objs=request.user.starmodel_set.all()
        for obj in objs:
            if obj.flag=='1':
                star_ids.append(obj.life_id)
        lives=LifeModel.objects.filter(id__in=star_ids)
        collection_ids=[]
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
        return render(request, 'pieces/star_life.html', {'page_content': page_content,
                                                        'page_list': page_list,
                                                        'current_page': page_content.number,
                                                        'num_pages': num_pages,
                                                         'collection_ids':collection_ids})
#点赞文章列表页面
class CollectLifeList(View):
    def get(self,request):
        page_number = int(request.GET.get('page_number', 1))
        collection_ids=[]
        objs=request.user.collectionmodel_set.all()
        for obj in objs:
            if obj.flag=='1':
                collection_ids.append(obj.life_id)
        lives=LifeModel.objects.filter(id__in=collection_ids)
        star_ids=[]
        for life in lives:
            objs=request.user.collectionmodel_set.all()
            for obj in objs:
                if obj.life==life and obj.flag=='1':
                    star_ids.append(life.id)
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
        return render(request, 'pieces/collect_life.html', {'page_content': page_content,
                                                        'page_list': page_list,
                                                        'current_page': page_content.number,
                                                        'num_pages': num_pages,
                                                         'star_ids':star_ids})
class LifeSearchView(SearchView):

    template = 'search/life_search.html'
    results = EmptySearchQuerySet()
    results_per_page = 2
    def __init__(self):
        from haystack.query import SearchQuerySet
        sqs=SearchQuerySet().using('life')
        super(LifeSearchView, self).__init__(searchqueryset=sqs)
    def get_query(self):
        queryset=super(LifeSearchView, self).get_query()
        return queryset
    def get_results(self):
        result=[]
        for obj in self.form.search():
            if obj.model_name == 'lifemodel':
                result.append(obj)
        return result
    def get_context(self):
        (paginator, page) = self.build_page()
        num_pages = paginator.num_pages
        page_number = int(self.request.GET.get('page', 1))
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
        piece_list = []

        star_ids = []  # 接受用户已点过赞的视频
        collection_ids = []  # 接受用户已收藏的视频
        for life in page:
            piece_list.append(life.object)
            stars_obj = life.object.starmodel_set.all()
            collections_obj = life.object.collectionmodel_set.all()
            for obj in stars_obj:
                if obj.user == self.request.user and obj.flag=='1':
                    star_ids.append(obj.life_id)
            for obj in collections_obj:
                if obj.user == self.request.user and obj.flag=='1':
                    collection_ids.append(obj.life_id)

        context = {
            "query": self.query,
            "form": self.form,
            "page": page,
            "page_list": page_list,
            "piece_list": piece_list,
            'current_page': page.number,
            'num_pages': num_pages,
            "paginator": paginator,
            "q": self.get_query(),
            "suggestion": None,
            "star_ids": star_ids,
            "collection_ids": collection_ids,
        }

        if (
                hasattr(self.results, "query")
                and self.results.query.backend.include_spelling
        ):
            context["suggestion"] = self.form.get_suggestion()
        return context

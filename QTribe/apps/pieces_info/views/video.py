# 上传视频
import os
import subprocess

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator, InvalidPage
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse, Http404
from django.shortcuts import redirect, render
from django.views import View
from haystack.query import EmptySearchQuerySet
from haystack.views import SearchView

from pieces_info.models import VideoModel, ImageModel

from user.models import StarModel, CollectionModel

from QTribe.tasks import send_message


class UploadVideo(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'pieces/upload_video.html')

    def post(self, request):
        # data=json.loads(request.body)
        title = request.POST.get('title')
        remark = request.POST.get('remark')
        video_path = request.FILES.get('video')

        if not video_path:  # 上传失败
            return JsonResponse({'code': 401})

        video_obj = VideoModel.objects.create(title=title, remark=remark, video=video_path, user=request.user)
        video_operator(request, video_obj.id,
                       video_path=os.path.join(settings.BASE_DIR2, 'media', video_obj.video.name),
                       img_path=os.path.join(settings.BASE_DIR2, 'media', f'{video_obj.video.name}{video_obj.id}.jpg'))

        # 上传成功
        return JsonResponse({'code': 200})


def run_cmd(cmd1, cmd2):
    """运行命令"""
    flag1 = False
    flag2 = False
    play_time = '0'
    result1 = subprocess.run(cmd1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='gbk', shell=True)
    result2 = subprocess.run(cmd2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='gbk', shell=True)

    if result1.returncode == 0:
        print('播放时长命令完成')
        flag1 = True
        long_time = result1.stdout
        # 需要截取整数部分
        play_time = long_time[:long_time.find('.')]  # 返回播放时长的数值
    else:
        print('播放时长命令执行错误')
        print(result1)
    if result2.returncode == 0:
        print('截取图片命令完成')
        flag2 = True
    else:
        print('截取图片命令执行错误')
        print(result2)

    if flag1 and flag2:
        return True, int(play_time)
    else:
        return False, int(play_time)


def video_operator(request, video_id, video_path, img_path):
    """视频处理,就是拼凑好两条ffmpeg的命令"""
    # 拼凑播放时长的命令
    cmd1 = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i {video_path}'
    # 拼凑截取图片的命令，固定：截取视频中第5秒图片
    cmd2 = f'ffmpeg -ss 00:00:05 -i {video_path} -vframes 1 {img_path}'
    print(cmd1)
    print(cmd2)
    result = run_cmd(cmd1, cmd2)  # 使用单独的进程执行命令

    # 如果命令正常执行，则修改数据库中video记录（增加预览图片路径和播放时长）
    if result[0]:
        # 得到图片的名字
        image_name = os.path.basename(img_path)
        image_path = '/media/' + image_name
        # 得到视频播放时长
        play_time = '%02d:%02d' % (int(result[1] / 60), result[1] % 60)
        with transaction.atomic():
            video = VideoModel.objects.filter(id=video_id).update(img_path=image_path, duration_time=play_time,
                                                                  is_success=True)

            ImageModel.objects.create(image_path=image_path, video_id=video_id, user=request.user)


# 自己的视频列表页面
class MyVideo(View):
    def get(self, request):

        page_number = int(request.GET.get('page_number', 1))
        # 获取该用户所有视频
        video_list = VideoModel.objects.filter(user__id=request.user.id)
        # 创建分页对象
        paginator = Paginator(video_list, 5)
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
        return render(request, 'pieces/my_video.html', {'page_content': page_content,
                                                        'page_list': page_list,
                                                        'current_page': page_content.number,
                                                        'num_pages': num_pages})


# 播放视频,浏览次数
class PlayVideo(View):
    def post(self, request):
        v_id = int(request.POST.get('v_id'))
        VideoModel.objects.filter(id=v_id).update(running_count=F('running_count') + 1)
        return JsonResponse({"data": "success"})


# 视频点赞量
class StarVideo(View):
    def get(self, request):
        v_id = int(request.GET.get('v_id'))
        args = request.GET.get('args')  # 判断是从看点广场页面进入，还是从点赞列表页面进入
        current_page = int(request.GET.get('current_page'))
        q=request.GET.get('q')
        video = VideoModel.objects.get(id=v_id)
        try:
            is_star = StarModel.objects.get(user_id=request.user.id, video_id=v_id)
            flag=is_star.flag
        except:
            is_star=0
        if is_star and flag=='1':
            video.star_count -= 1
            video.save()
            is_star.flag = '0'
            is_star.save()
            if args == 'mall':
                return redirect(f'/index/video_mall?page_number={current_page}')
            if args == 'star':  # 有可能用户取消点赞后，当页就没有内容，防止报错，加一个try
                try:
                    return redirect(f'/pieces/star_video_list?page_number={current_page}')
                except:
                    return redirect(f'/pieces/star_video_list?page_number={current_page - 1}')
            if args == 'collect':
                return redirect(f'/pieces/collect_video_list?page_number={current_page}')
            if args=='search':
                return redirect(f'/pieces/search_video/?page={current_page}&q={q}')

        else:
            video.star_count += 1
            video.save()
            data={'u_id':request.user.id,'type_2':'star_video','p_id':v_id}
            send_message.delay(data)
            if not is_star:
                StarModel.objects.create(user=request.user, video=video,flag='1')
            else:
                is_star.flag = '1'
                is_star.save()
            if args == 'mall':
                return redirect(f'/index/video_mall?page_number={current_page}')
            if args == 'collect':
                return redirect(f'/pieces/collect_video_list?page_number={current_page}')
            if args=='search':
                return redirect(f'/pieces/search_video/?page={current_page}&q={q}')


# 视频收藏量
class CollectVideo(View):
    def get(self, request):
        v_id = int(request.GET.get('v_id'))
        current_page = int(request.GET.get('current_page'))
        args = request.GET.get('args')  # 判断是从看点广场页面进入，还是从收藏列表页面进入
        q=request.GET.get('q')
        video = VideoModel.objects.get(id=v_id)
        try:
            is_collect = CollectionModel.objects.get(user_id=request.user.id, video_id=v_id)
            flag=is_collect.flag
        except:
            is_collect=0
        if is_collect and flag=='1':
            video.collection_count -= 1
            video.save()
            is_collect.flag='0'
            is_collect.save()
            if args == 'mall':
                return redirect(f'/index/video_mall?page_number={current_page}')
            if args == 'collect':
                try:
                    return redirect(f'/pieces/collect_video_list?page_number={current_page}')
                except:
                    return redirect(f'/pieces/collect_video_list?page_number={current_page - 1}')
            if args == 'star':
                return redirect(f'/pieces/star_video_list?page_number={current_page}')
            if args=='search':
                return redirect(f'/pieces/search_video/?page={current_page}&q={q}')
        else:
            video.collection_count += 1
            video.save()
            data={'u_id':request.user.id,'type_2':'collect_video','p_id':v_id}
            send_message.delay(data)
            if not is_collect:
                CollectionModel.objects.create(user=request.user, video=video,flag='1')
            else:
                is_collect.flag = '1'
                is_collect.save()
            if args == 'mall':
                return redirect(f'/index/video_mall?page_number={current_page}')
            if args == 'star':
                return redirect(f'/pieces/star_video_list?page_number={current_page}')
            if args=='search':
                return redirect(f'/pieces/search_video/?page={current_page}&q={q}')

# 视频顶置
class TopVideo(View):
    def get(self, request):
        v_id = int(request.GET.get('v_id'))
        is_top = int(request.GET.get('is_top'))
        current_page = int(request.GET.get('current_page'))
        if is_top == 1:
            VideoModel.objects.filter(id=v_id).update(is_top=0)
            return redirect(f'/pieces/my_video?page_number={current_page}')
        if is_top == 0:
            VideoModel.objects.filter(id=v_id).update(is_top=1)
            return redirect(f'/pieces/my_video?page_number={current_page}')


# 删除视频
class DeleteVideo(View):
    def get(self, request):
        v_id = int(request.GET.get('v_id'))
        current_page = int(request.GET.get('current_page'))
        VideoModel.objects.filter(id=v_id).delete()
        try:
            return redirect(f'/pieces/my_video?page_number={current_page}')
        except:
            return redirect(f'/pieces/my_video?page_number={current_page - 1}')


# 点赞的视频列表页面
class StarVideoList(View):
    def get(self, request):
        page_number = int(request.GET.get('page_number', 1))
        star_ids = []
        objs = request.user.starmodel_set.all()
        for obj in objs:
            if obj.flag=='1':
                star_ids.append(obj.video_id)
        # 获取该用户所有点赞过的视频
        video_list = VideoModel.objects.filter(id__in=star_ids)
        collection_ids = []  # 用于筛选用户收藏过的视频，方便前端渲染
        for video in video_list:
            objs = request.user.collectionmodel_set.all()
            for obj in objs:
                if obj.video == video and obj.flag=='1':
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
        return render(request, 'pieces/star_video.html', {'page_content': page_content,
                                                          'page_list': page_list,
                                                          'current_page': page_content.number,
                                                          'num_pages': num_pages,
                                                          'collection_ids': collection_ids})


# 收藏的视频列表页面
class CollectVideoList(View):
    def get(self, request):
        page_number = int(request.GET.get('page_number', 1))
        collection_ids = []
        objs = request.user.collectionmodel_set.all()
        for obj in objs:
            if obj.flag=='1':
                collection_ids.append(obj.video_id)
        # 获取该用户所有收藏的视频
        video_list = VideoModel.objects.filter(id__in=collection_ids)
        star_ids = []  # 用于筛选用户点赞过的视频，方便前端渲染
        for video in video_list:
            objs = request.user.starmodel_set.all()
            for obj in objs:
                if obj.video == video and obj.flag=='1':
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

        return render(request, 'pieces/collect_video.html', {'page_content': page_content,
                                                             'page_list': page_list,
                                                             'current_page': page_content.number,
                                                             'num_pages': num_pages,
                                                             'star_ids': star_ids})

#搜索引擎
class VideoSearchView(SearchView):

    template = 'search/video_search.html'
    results = EmptySearchQuerySet()
    results_per_page = 2
    def __init__(self):
        from haystack.query import SearchQuerySet
        sqs=SearchQuerySet().using('video')
        super(VideoSearchView, self).__init__(searchqueryset=sqs)
    def get_query(self):
        queryset=super(VideoSearchView, self).get_query()
        return queryset
    def get_results(self):
        result=[]
        for obj in self.form.search():
            if obj.model_name == 'videomodel':
                result.append(obj)
        return result
    def get_context(self):
        (paginator, page) = self.build_page()
        num_pages = paginator.num_pages
        page_number=int(self.request.GET.get('page',1))
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
        piece_list=[]#接受查询到的对象
        star_ids=[]#接受用户已点过赞的视频
        collection_ids=[]#接受用户已收藏的视频
        for video in page:
            piece_list.append(video.object)
            stars_obj=video.object.starmodel_set.all()
            collections_obj=video.object.collectionmodel_set.all()
            for obj in stars_obj:
                if obj.user==self.request.user:
                    star_ids.append(obj.video_id)
            for obj in collections_obj:
                if obj.user==self.request.user:
                    collection_ids.append(obj.video_id)

        context = {
            "query": self.query,
            "form": self.form,
            "page": page,
            "page_list":page_list,
            "piece_list": piece_list,
            'current_page': page.number,
            'num_pages': num_pages,
            "paginator": paginator,
            "q":self.get_query(),
            "suggestion": None,
            "star_ids":star_ids,
            "collection_ids":collection_ids,
        }

        if (
            hasattr(self.results, "query")
            and self.results.query.backend.include_spelling
        ):
            context["suggestion"] = self.form.get_suggestion()
        return context

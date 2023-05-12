import json
import os
import subprocess

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from pieces_info.models import VideoModel

from pieces_info.models import ImageModel


class UploadVideo(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'pieces/upload_video.html')

    def post(self, request):
        # data=json.loads(request.body)
        title=request.POST.get('title')
        remark=request.POST.get('remark')
        video_path=request.FILES.get('video')
        print('title----------->',title)
        print('remark----------->',remark)
        print('video_path----------->',video_path)
        # title = data['title']
        # remark = data['remark']
        # video_path = data['video']
        if not video_path:#上传失败
            return JsonResponse({'code':401})

        video_obj=VideoModel.objects.create(title=title, remark=remark, video=video_path, user=request.user)
        video_operator(video_obj.id,
                       video_path=os.path.join(settings.BASE_DIR2,'media',video_obj.video.name),
                       img_path=os.path.join(settings.BASE_DIR2,'media',f'{video_obj.id}.jpg'))

        #上传成功
        return JsonResponse({'code':200})
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


def video_operator(video_id, video_path, img_path):
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
        # 得到视频播放时长
        play_time = '%02d:%02d' % (int(result[1] / 60), result[1] % 60)
        # 修改数据库的数据，注意：is_success修改为Ture
        VideoModel.objects.filter(id=video_id).update(img_path=image_name, duration_time=play_time)

#自己的视频列表页面
class MyVideo(View):
    def get(self,request):

        page_number = int(request.GET.get('page_number', 1))
        # 获取该用户所有视频
        video_list = VideoModel.objects.filter(user__id=request.user.id)
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
        return render(request, 'pieces/my_video.html', {'page_content': page_content,
                                                        'page_list': page_list,
                                                        'current_page': page_content.number,
                                                        'num_pages': num_pages})

#自己的文章列表页面
class MyArticle(View):
    def get(self,request):
        return render(request,'pieces/my_article.html')

#自己的生活列表页面
class MyLife(View):
    def get(self,request):
        return render(request,'pieces/my_life.html')

#上传图片
class UploadImage(View):
    def post(self,request):
        try:
            image=request.FILES.get('image')
            request.user.icon=image
            request.user.save()
            img=ImageModel.objects.create(image=image,user=request.user)
            return JsonResponse({'code':200})
        except:
            return JsonResponse({'code':401})
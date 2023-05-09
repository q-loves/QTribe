import os
import subprocess

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from pieces_info.models import VideoModel


class UploadVideo(View):
    def get(self, request):
        return render(request, 'pieces/upload_video.html')

    def post(self, request):
        title = request.POST['title']
        remark = request.POST['remark']
        video = request.FILES.get('video')
        if not video:
            return HttpResponse('文件不存在')

        video_obj=VideoModel.objects.create(title=title, remark=remark, video=video, user=request.user)
        video_operator(video_obj.id,
                       video_path=os.path.join(settings.BASE_DIR,'media',video_obj.video.name),
                       img_path=os.path.join(settings.BASE_DIR,'media',f'{video_obj.id}.jpg'))
        return HttpResponse('上传成功')
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

from django.db import models

# Create your models here.
from QTribe.utils.base_model import BaseModel2

class CategoryModel(models.Model):
    name=models.CharField(verbose_name='类别名称',max_length=16,blank=True,null=True)
    class Meta:
        db_table = 't_category'
        verbose_name = '类型'
        verbose_name_plural = verbose_name


class ArticleModel(BaseModel2):
    """文章"""
    title = models.CharField(max_length=100,unique=True,verbose_name='文章标题')
    content = models.TextField(verbose_name='文章内容')
    default_img = models.ImageField(verbose_name='首页图片',blank=True,null=True)
    running_count = models.IntegerField(verbose_name='浏览次数', max_length=20, null=True, blank=True, default=0)
    star_count = models.IntegerField(default=0,verbose_name='点赞量',blank=True,null=True)
    collection_count = models.IntegerField(default=0, verbose_name='收藏量', blank=True, null=True)
    comment_count = models.IntegerField(default=0,verbose_name='评论量',blank=True,null=True)
    category=models.ForeignKey('CategoryModel',on_delete=models.CASCADE,verbose_name='文章类型',blank=True,null=True,related_name='article')
    user=models.ForeignKey('user.UserModel',on_delete=models.CASCADE,verbose_name='作者',related_name='article')
    is_top = models.IntegerField(verbose_name='是否置顶', default=0)
    class Meta:
        db_table = 't_article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-is_top', '-id']
    def __str__(self):
        return self.title

class VideoModel(BaseModel2):
    video=models.FileField(verbose_name='视频内容')
    title = models.CharField(verbose_name='视频标题', max_length=20, null=True, blank=True)
    star_count = models.IntegerField(default=0, verbose_name='点赞量', blank=True, null=True)
    collection_count = models.IntegerField(default=0, verbose_name='收藏量', blank=True, null=True)
    comment_count = models.IntegerField(default=0, verbose_name='评论量', blank=True, null=True)
    category = models.ForeignKey('CategoryModel', on_delete=models.CASCADE, verbose_name='视频类型', blank=True, null=True,
                                 related_name='video')
    duration_time=models.CharField(verbose_name='视频时长',max_length=20,null=True,blank=True)
    remark=models.CharField(verbose_name='备注',max_length=50,null=True,blank=True)
    img_path = models.CharField(verbose_name='照片文件', max_length=256, null=True, blank=True)
    running_count = models.IntegerField(verbose_name='播放次数', max_length=20, null=True, blank=True,default=0)
    user = models.ForeignKey('user.UserModel', verbose_name='用户', on_delete=models.CASCADE, related_name='video')
    is_top=models.IntegerField(verbose_name='是否置顶',default=0)
    is_success=models.BooleanField(verbose_name='是否发布成功',null=True,blank=True,max_length=4)
    class Meta:
        db_table = 't_video'
        verbose_name = '视频'
        verbose_name_plural = verbose_name
        ordering=['-is_top','-id']

class LifeModel(BaseModel2):
    copy=models.CharField(verbose_name='文案',max_length=512)
    user = models.ForeignKey('user.UserModel', on_delete=models.CASCADE, verbose_name='作者', related_name='life')
    default_img = models.ImageField(verbose_name='首页图片', blank=True, null=True)
    star_count = models.IntegerField(default=0, verbose_name='点赞量', blank=True, null=True)
    collection_count = models.IntegerField(default=0, verbose_name='收藏量', blank=True, null=True)
    comment_count = models.IntegerField(default=0, verbose_name='评论量', blank=True, null=True)
    is_top = models.IntegerField(verbose_name='是否置顶', default=0)
    is_friend = models.IntegerField(verbose_name='是否仅好友可见', default=0)
    status=models.CharField(verbose_name='作者状态1.阅读2.创作3.开心4.emo5.发呆',blank=True,null=True,max_length=4)
    running_count = models.IntegerField(verbose_name='播放次数', max_length=20, null=True, blank=True, default=0)
    class Meta:
        db_table = 't_life'
        verbose_name = '生活琐事'
        verbose_name_plural = verbose_name
        ordering=['-is_top','-id']

class ImageModel(BaseModel2):
    image=models.ImageField(verbose_name='图片内容',blank=True,null=True)#用户头像，文章图像，生活照片
    image_path=models.CharField(verbose_name='图片相对路径',max_length=256,blank=True,null=True)#视频截取图片
    video=models.ForeignKey('VideoModel',verbose_name='视频',on_delete=models.CASCADE,blank=True,null=True,related_name='image')
    article=models.ForeignKey('ArticleModel',verbose_name='文章',on_delete=models.CASCADE,blank=True,null=True,related_name='image')
    life=models.ForeignKey('LifeModel',on_delete=models.CASCADE,verbose_name='生活琐事',blank=True,null=True,related_name='image')
    user=models.ForeignKey('user.UserModel',verbose_name='用户',on_delete=models.CASCADE,related_name='image')

    class Meta:
        db_table='t_image'
        verbose_name='图片'
        verbose_name_plural=verbose_name

class CommentModel(BaseModel2):
    content=models.CharField(verbose_name='评论内容',max_length=128)
    article=models.ForeignKey('ArticleModel',on_delete=models.CASCADE,related_name='comment',blank=True,null=True)
    video=models.ForeignKey('VideoModel',on_delete=models.CASCADE,related_name='comment',blank=True,null=True)
    life = models.ForeignKey('LifeModel', on_delete=models.CASCADE, verbose_name='生活琐事', blank=True, null=True,related_name='comment')
    user=models.ForeignKey('user.UserModel',verbose_name='用户',on_delete=models.CASCADE,related_name='comment')
    class Meta:
        db_table = 't_comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name

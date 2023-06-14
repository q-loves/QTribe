from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from QTribe.utils.base_model import BaseModel2


class UserModel(AbstractUser,BaseModel2):

    phone=models.CharField(verbose_name='电话号码',max_length=11,unique=True)
    icon=models.ImageField(verbose_name='用户头像',blank=True,null=True)
    personalized_signature=models.CharField(verbose_name='个性签名',max_length=256,blank=True,null=True)
    personal_introduce=models.CharField(verbose_name='个人介绍',max_length=1024,blank=True,null=True)
    province=models.CharField(verbose_name='省份',max_length=8,blank=True,null=True)
    city=models.CharField(verbose_name='城市',max_length=8,blank=True,null=True)
    county=models.CharField(verbose_name='县区',max_length=8,blank=True,null=True)
    sex=models.CharField(verbose_name='性别',max_length=2,default='1')
    age=models.IntegerField(verbose_name='年龄',blank=True,null=True)

    class Meta:
        db_table='t_user'
        verbose_name='用户表'
        verbose_name_plural=verbose_name

class FocusModel(BaseModel2):
    user=models.ForeignKey('UserModel',on_delete=models.CASCADE,verbose_name='用户')
    focus_user=models.ForeignKey('UserModel',on_delete=models.CASCADE,verbose_name='被关注用户',related_name='focus_user')
    #避免用户重复关注，取消关注，浪费数据库资源。每当用户关注或取消关注时，只对flag进行操作，不会浪费数据库内存
    flag=models.CharField(verbose_name='标志',max_length=2,blank=True,null=True)
    class Meta:
        db_table='t_focus_uer'
        verbose_name='关注列表'
        verbose_name_plural=verbose_name

class FriendModel(BaseModel2):
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE, verbose_name='发起申请用户')
    friend_user = models.ForeignKey('UserModel', on_delete=models.CASCADE, verbose_name='通过申请用户',
                                   related_name='friend_user')
    # 避免用户重复添加，删除好友，浪费数据库资源。每当用户添加或删除时，只对flag进行操作，不会浪费数据库内存
    flag = models.CharField(verbose_name='标志', max_length=2, blank=True, null=True)

    class Meta:
        db_table = 't_friend_uer'
        verbose_name = '好友列表'
        verbose_name_plural = verbose_name

class StarModel(BaseModel2):
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE, verbose_name='用户')
    video = models.ForeignKey('pieces_info.VideoModel', on_delete=models.CASCADE, verbose_name='点赞视频',blank=True,null=True)
    article = models.ForeignKey('pieces_info.ArticleModel', on_delete=models.CASCADE, verbose_name='点赞文章',blank=True,null=True)
    life = models.ForeignKey('pieces_info.LifeModel', on_delete=models.CASCADE, verbose_name='生活琐事', blank=True, null=True)
    flag=models.CharField(verbose_name='标志',max_length=2,blank=True,null=True)
    class Meta:
        db_table = 't_star_uer'
        verbose_name = '点赞列表'
        verbose_name_plural = verbose_name

class CollectionModel(BaseModel2):
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE, verbose_name='用户')
    video = models.ForeignKey('pieces_info.VideoModel', on_delete=models.CASCADE, verbose_name='收藏视频',blank=True,null=True)
    article = models.ForeignKey('pieces_info.ArticleModel', on_delete=models.CASCADE, verbose_name='收藏文章',blank=True,null=True)
    life = models.ForeignKey('pieces_info.LifeModel', on_delete=models.CASCADE, verbose_name='收藏生活',blank=True,null=True)
    flag = models.CharField(verbose_name='标志', max_length=2, blank=True, null=True)
    class Meta:
        db_table = 't_collection_uer'
        verbose_name = '收藏列表'
        verbose_name_plural = verbose_name
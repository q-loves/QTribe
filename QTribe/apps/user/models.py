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
    class Meta:
        db_table='t_focus_uer'
        verbose_name='关注列表'
        verbose_name_plural=verbose_name


class StarModel(BaseModel2):
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE, verbose_name='用户')
    video = models.ForeignKey('pieces_info.VideoModel', on_delete=models.CASCADE, verbose_name='点赞视频',blank=True,null=True)
    article = models.ForeignKey('pieces_info.ArticleModel', on_delete=models.CASCADE, verbose_name='点赞文章',blank=True,null=True)

    class Meta:
        db_table = 't_star_uer'
        verbose_name = '点赞列表'
        verbose_name_plural = verbose_name

class CollectionModel(BaseModel2):
    user = models.ForeignKey('UserModel', on_delete=models.CASCADE, verbose_name='用户')
    video = models.ForeignKey('pieces_info.VideoModel', on_delete=models.CASCADE, verbose_name='收藏视频',blank=True,null=True)
    article = models.ForeignKey('pieces_info.ArticleModel', on_delete=models.CASCADE, verbose_name='收藏文章',blank=True,null=True)
    # life = models.ForeignKey('pieces.LifeModel', on_delete=models.CASCADE, verbose_name='收藏生活',blank=True,null=True)

    class Meta:
        db_table = 't_collection_uer'
        verbose_name = '收藏列表'
        verbose_name_plural = verbose_name
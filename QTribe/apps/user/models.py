from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from QTribe.utils.base_model import BaseModel


class UserModel(AbstractUser,BaseModel):

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


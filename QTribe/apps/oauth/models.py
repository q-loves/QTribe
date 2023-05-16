from django.db import models

# Create your models here.
from QTribe.utils.base_model import BaseModel


class QQUser(BaseModel):
    user=models.ForeignKey('user.UserModel',on_delete=models.CASCADE,verbose_name='qq用户')
    openid=models.CharField(verbose_name='openid',max_length=64,db_index=True)

    class Meta:
        db_table='t_qq_user'
        verbose_name='QQ用户'
        verbose_name_plural=verbose_name

class WeChatUser(BaseModel):
    user=models.ForeignKey('user.UserModel',on_delete=models.CASCADE,verbose_name='qq用户')
    openid=models.CharField(verbose_name='openid',max_length=64,db_index=True)

    class Meta:
        db_table='t_wechat_user'
        verbose_name='微信用户'
        verbose_name_plural=verbose_name
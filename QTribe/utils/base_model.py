from django.db import models
import datetime

class BaseModel2(models.Model):
    create_time=models.DateTimeField(verbose_name='添加时间',auto_now_add=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    update_time=models.DateTimeField(verbose_name='修改时间',auto_now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    class Meta:
        abstract=True
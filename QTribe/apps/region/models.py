from django.db import models

# Create your models here.
class Nation(models.Model):
    n_name = models.CharField('国家名称', max_length=30)

    class Meta:
        db_table = 'nation'
        verbose_name = '国家表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.n_name


# 省份的模型类
class Province(models.Model):
    p_name = models.CharField('省份名称', max_length=30)
    nation = models.ForeignKey('Nation', related_name='province_list', on_delete=models.CASCADE, verbose_name='省份所在的国家')

    class Meta:
        db_table = 'province'
        verbose_name = '省份表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.p_name


# 城市的模型类
class City(models.Model):
    c_name = models.CharField('城市名称', max_length=30)
    province = models.ForeignKey('Province', related_name='city_list', on_delete=models.CASCADE, verbose_name='城市所在的省份')

    class Meta:
        db_table = 'city'
        verbose_name = '城市表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.c_name

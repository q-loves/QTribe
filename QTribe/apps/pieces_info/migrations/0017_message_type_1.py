# Generated by Django 4.2.2 on 2023-06-08 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pieces_info', '0016_commentmodel_comment_message_comment_message_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='type_1',
            field=models.CharField(default='1', max_length=4, verbose_name='信息类型1.点赞2.收藏3.评论4.关注5.好友申请6.好友通过'),
        ),
    ]
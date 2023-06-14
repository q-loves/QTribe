# Generated by Django 4.2.2 on 2023-06-10 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_starmodel_collectionmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('flag', models.CharField(blank=True, max_length=2, null=True, verbose_name='标志')),
                ('friend_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_user', to=settings.AUTH_USER_MODEL, verbose_name='通过申请用户')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='发起申请用户')),
            ],
            options={
                'verbose_name': '好友列表',
                'verbose_name_plural': '好友列表',
                'db_table': 't_friend_uer',
            },
        ),
    ]
# Generated by Django 3.2.15 on 2023-05-16 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pieces_info', '0004_auto_20230513_0845'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='articlemodel',
            options={'ordering': ['is_top', 'id'], 'verbose_name': '文章', 'verbose_name_plural': '文章'},
        ),
        migrations.AlterModelOptions(
            name='videomodel',
            options={'ordering': ['is_top', 'id'], 'verbose_name': '视频', 'verbose_name_plural': '视频'},
        ),
        migrations.AddField(
            model_name='articlemodel',
            name='is_top',
            field=models.IntegerField(default=0, verbose_name='是否置顶'),
        ),
        migrations.AddField(
            model_name='videomodel',
            name='is_success',
            field=models.BooleanField(blank=True, max_length=4, null=True, verbose_name='是否发布成功'),
        ),
        migrations.AddField(
            model_name='videomodel',
            name='is_top',
            field=models.IntegerField(default=0, verbose_name='是否置顶'),
        ),
        migrations.AlterField(
            model_name='videomodel',
            name='running_count',
            field=models.IntegerField(blank=True, default=0, max_length=20, null=True, verbose_name='播放次数'),
        ),
    ]

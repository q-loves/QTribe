# Generated by Django 3.2.15 on 2023-05-09 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pieces_info', '0003_auto_20230509_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='videomodel',
            name='title',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='视频标题'),
        ),
    ]

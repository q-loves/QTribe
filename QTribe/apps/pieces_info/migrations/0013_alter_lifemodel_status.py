# Generated by Django 3.2.15 on 2023-06-06 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pieces_info', '0012_alter_lifemodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lifemodel',
            name='status',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='作者状态'),
        ),
    ]
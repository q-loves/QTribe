# Generated by Django 3.2.15 on 2023-05-13 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='用户头像'),
        ),
    ]
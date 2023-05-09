# Generated by Django 3.2.15 on 2023-05-08 03:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('region', '0001_initial'),
        ('user', '0002_usermodel_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='region.city'),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='nation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='region.nation'),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='region.province'),
        ),
    ]

# Generated by Django 3.2.9 on 2021-12-12 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20211212_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='tacitrecord',
            name='tacit_reply_status',
            field=models.SmallIntegerField(choices=[(0, '广场可见'), (1, '主页可见'), (2, '个人可见')], default=0, verbose_name='回复控制状态'),
        ),
    ]

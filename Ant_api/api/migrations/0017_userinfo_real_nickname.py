# Generated by Django 3.2.9 on 2021-12-08 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20211209_0309'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='real_nickName',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='用户昵称'),
        ),
    ]

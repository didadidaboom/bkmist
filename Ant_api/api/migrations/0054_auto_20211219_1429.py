# Generated by Django 3.2.9 on 2021-12-19 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_tacitreplyviewer'),
    ]

    operations = [
        migrations.AddField(
            model_name='tacitreplyviewer',
            name='source',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='来源'),
        ),
        migrations.AddField(
            model_name='tacitreplywrite',
            name='source',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='来源'),
        ),
    ]

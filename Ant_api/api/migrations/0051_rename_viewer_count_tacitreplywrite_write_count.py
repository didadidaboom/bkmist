# Generated by Django 3.2.9 on 2021-12-17 02:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_auto_20211217_0204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tacitreplywrite',
            old_name='viewer_count',
            new_name='write_count',
        ),
    ]

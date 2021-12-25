import os
import sys
import django



base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","Ant_api.settings")
django.setup()

from api import models
'''
for index in range(11):
    models.TopicInfo.objects.create(
        title = "新加坡留学{}".format(index),
        user_id = 1)
'''
models.TopicInfo.objects.create(
        title = "NTU",
        description ="一个QS排名10左右美丽的大学",
        user_id = 1)
#models.TopicInfo.objects.all().delete()
#models.TopicInfo.objects.get(id=28).delete()
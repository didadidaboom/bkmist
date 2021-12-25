import os
import sys
import django



base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","Ant_api.settings")
django.setup()

from api import models

models.TacitTestDatabase.objects.create(
    title="我觉得朋友的最高境界是什么?",
    answer1="形影不离",
    answer2="分享秘密话题",
    answer3="一起经历事情",
    answer4="一起成长"
)
import os
import sys
import django



base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","Ant_api.settings")
django.setup()

from api import models
'''
models.UserInfo.objects.create(
        phone=18801072898,
        nickName='CHONG',
        avatarUrl="https://mini-1257058751.cos.ap-chengdu.myqcloud.com/publish/rKjmS73u9rxE4841cbe02d57adc848fac938c2a75dd1.jpg"
)
'''
for index in range(8):
        models.UserInfo.objects.create(
                phone=18801072890+index,
                nickName='CHONG{}'.format(index),
                avatarUrl="https://mini-1257058751.cos.ap-chengdu.myqcloud.com/publish/rKjmS73u9rxE4841cbe02d57adc848fac938c2a75dd1.jpg"
        )

#models.UserInfo.objects.get(id=3).delete()
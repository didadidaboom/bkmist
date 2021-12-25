import os
import sys
import django



base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","Ant_api.settings")
django.setup()

from api import models
'''
for index in range(50):
    obj = models.Moment.objects.create(
        content = "新加坡真的太热了{}".format(index),
        user_id=1,
        topic_id=20,
        address="新加坡"
    )
    models.MomentDetail.objects.create(
        path="https://mini-1257058751.cos.ap-chengdu.myqcloud.com/publish/76QZakn3MHuF4761b10b8002106a7817395f9d856619.jpg",
        path_key="76QZakn3MHuF4761b10b8002106a7817395f9d856619.jpg",
        moment_id=obj.id
    )
    models.MomentDetail.objects.create(
        path="https://mini-1257058751.cos.ap-chengdu.myqcloud.com/publish/rKjmS73u9rxE4841cbe02d57adc848fac938c2a75dd1.jpg",
        path_key="rKjmS73u9rxE4841cbe02d57adc848fac938c2a75dd1.jpg",
        moment_id=obj.id
    )
'''
#obj = models.Moment.objects.all().delete()
#for idx in range(44,66):
#    models.CommentRecord.objects.get(id=idx).delete()
models.Moment.objects.get(id=25).delete()
'''
obj = models.Moment.objects.create(
    content = "kaws快结束了。。。",
    user_id=9,
    topic_id=28,
    address="新加坡"
)
models.MomentDetail.objects.create(
    path="https://mini-1257058751.cos.ap-chengdu.myqcloud.com/publish/76QZakn3MHuF4761b10b8002106a7817395f9d856619.jpg",
    path_key="76QZakn3MHuF4761b10b8002106a7817395f9d856619.jpg",
    moment_id=obj.id
)
models.MomentDetail.objects.create(
    path="https://mini-1257058751.cos.ap-chengdu.myqcloud.com/publish/rKjmS73u9rxE4841cbe02d57adc848fac938c2a75dd1.jpg",
    path_key="rKjmS73u9rxE4841cbe02d57adc848fac938c2a75dd1.jpg",
    moment_id=obj.id
)
'''
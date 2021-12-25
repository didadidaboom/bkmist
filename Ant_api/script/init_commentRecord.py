import os
import sys
import django



base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","Ant_api.settings")
django.setup()

from api import models
'''
first1 = models.CommentRecord.objects.create(
    moment_id=61,
    content="1",
    user_id=1,
    depth=1,
    #root_id=null
)

first1_1 = models.CommentRecord.objects.create(
    moment_id=61,
    content="1_1",
    user_id=7,
    depth=2,
    reply=first1,
    root=first1
)
first1_1_1 = models.CommentRecord.objects.create(
    moment_id=61,
    content="1_1_1",
    user_id=6,
    depth=3,
    reply=first1_1,
    root=first1
)
first1_1_1_1 = models.CommentRecord.objects.create(
    moment_id=61,
    content="1_1_1_1",
    user_id=1,
    depth=3,
    reply=first1_1_1,
    root=first1
)

first2 = models.CommentRecord.objects.create(
    moment_id=61,
    content="2",
    user_id=3,
    depth=1,
    #root_id=null
)
first2_1 = models.CommentRecord.objects.create(
    moment_id=61,
    content="2_1",
    user_id=6,
    depth=2,
    reply = first2,
    root = first2
)
first3 = models.CommentRecord.objects.create(
    moment_id=61,
    content="3",
    user_id=5,
    depth=1,
    #root_id=null
)
'''
#models.CommentRecord.objects.get(id=57).delete()
models.CommentRecord.objects.all().delete()


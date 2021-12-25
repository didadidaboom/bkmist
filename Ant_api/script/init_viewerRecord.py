import os
import sys
import django



base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","Ant_api.settings")
django.setup()

from api import models

models.ViewerRecord.objects.create(
    moment_id=61,
    user_id=1
)
models.ViewerRecord.objects.create(
    moment_id=61,
    user_id=3
)
models.ViewerRecord.objects.create(
    moment_id=61,
    user_id=5
)
models.ViewerRecord.objects.create(
    moment_id=61,
    user_id=7
)
models.ViewerRecord.objects.create(
    moment_id=61,
    user_id=6
)
models.ViewerRecord.objects.create(
    moment_id=61,
    user_id=6
)
models.ViewerRecord.objects.create(
    moment_id=61,
    user_id=1
)
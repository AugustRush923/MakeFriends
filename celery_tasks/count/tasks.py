from django.db.models import F
import logging

from celery_tasks.main import app
from blog.models import Post

logger = logging.getLogger('django')


@app.task(name='increase_both')
def increase_both(post_id):
    try:
        Post.objects.filter(id=post_id).update(pv=F('pv') + 1, uv=F('uv') + 1)
    except Exception as e:
        logger.error("异常出现")


@app.task(name='increase_PV')
def increase_PV(post_id):
    Post.objects.filter(id=post_id).update(pv=F('pv') + 1)


@app.task(name='increase_UV')
def increase_UV(post_id):
    Post.objects.filter(id=post_id).update(uv=F('uv') + 1)

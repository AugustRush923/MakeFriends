from django.db.models import F
from django_redis import get_redis_connection
import logging

from celery_tasks.main import app
from blog.models import Post

logger = logging.getLogger('django')
rds = get_redis_connection('hot_ranks')


@app.task(name='increase_both')
def increase_both(post_id):
    try:
        post = Post.objects.filter(id=post_id)
        post.update(pv=F('pv') + 1, uv=F('uv') + 1)
        if post[0].status:
            rds.zincrby('hot_rank', 1, f"{post[0].title}:{post[0].id}")  # db.zincrby(REDIS_KEY, increment, menber)
    except Exception as e:
        logger.error(f"异常出现: {e}")


@app.task(name='increase_PV')
def increase_PV(post_id):
    post = Post.objects.filter(id=post_id)
    post.update(pv=F('pv') + 1)
    if post[0].status:
        rds.zincrby('hot_rank', 1, f"{post[0].title}:{post[0].id}")


@app.task(name='increase_UV')
def increase_UV(post_id):
    Post.objects.filter(id=post_id).update(uv=F('uv') + 1)

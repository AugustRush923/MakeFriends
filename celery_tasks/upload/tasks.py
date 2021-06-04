from celery_tasks.main import app
import logging
from qiniu import Auth, put_file, CdnManager
from django.conf import settings

logger = logging.getLogger('django')


@app.task(name="upload_file")
def upload_file(file_path, bucket_name=settings.QINIU_BUCKET_NAME):
    key_name = "static/img/" + file_path.split("/")[-1]
    q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    token = q.upload_token(bucket=bucket_name, key=key_name)

    put_file(up_token=token, key=key_name, file_path=file_path)
    cdn_manger = CdnManager(q)
    urls = [
        'https://cdn.hdcheung.cn/static/img/wordcloud.png',
    ]
    cdn_manger.refresh_urls(urls)
    logger.info("上传并强制刷新成功")

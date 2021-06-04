from celery_tasks.upload.tasks import upload_file
from utils.WordCloud import wordCloud
import logging

logger = logging.getLogger('django')


def qiniu_upload(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        try:
            img_path = wordCloud.generate_word_cloud()
            upload_file.delay(img_path)
        except Exception as e:
            logger.error(f"上传失败,{e}")
        return result

    return wrapper

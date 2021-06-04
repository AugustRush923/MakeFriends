from django.core.signals import request_started
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
import uuid

from blog.models import Tag


# def my_callback(**kwargs):
#     print("Request Finished!")
#
#
# request_started.connect(my_callback, dispatch_uid=str(uuid.uuid4()))


@receiver(pre_save, sender=Tag, dispatch_uid=str(uuid.uuid4()))
def models_before_save_handler(sender, **kwargs):
    print("模型类保存之前执行操作...")


@receiver(pre_delete, sender=Tag, dispatch_uid=str(uuid.uuid4()))
def models_before_save_handler(sender, **kwargs):
    print("模型类删除之前执行操作...")

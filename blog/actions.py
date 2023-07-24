def make_status_normal(model_admin, requests, queryset):
    queryset.update(status=1)
    model_admin.message_user(requests, "修改成功！")


make_status_normal.short_description = "更改状态为正常"


def make_status_delete(model_admin, requests, queryset):
    queryset.update(status=0)
    model_admin.message_user(requests, "修改成功！")


make_status_delete.short_description = "更新状态为删除"


def save_all(model_admin, requests, queryset):
    for post in queryset:
        if post.status:
            post.save()
    model_admin.message_user(requests, "保存成功！")


save_all.short_description = "更新全部"

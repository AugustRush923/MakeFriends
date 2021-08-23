def make_status_normal(modeladmin, requests, queryset):
    queryset.update(status=1)
    modeladmin.message_user(requests, "修改成功！")


make_status_normal.short_description = "更改状态为正常"


def make_status_delete(modeladmin, requests, queryset):
    queryset.update(status=0)
    modeladmin.message_user(requests, "修改成功！")


make_status_delete.short_description = "更新状态为删除"

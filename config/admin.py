from django.contrib import admin
from .models import Link, SideBar


# Register your models here.


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'avatar', 'href', 'introduction', 'status', 'weight', 'created_time')
    fields = ('title', 'avatar', 'href', 'introduction', 'status', 'weight')
    list_filter = ('status',)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@admin.register(SideBar)
class SidebarAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SidebarAdmin, self).save_model(request, obj, form, change)

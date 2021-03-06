# -*- coding: utf-8 -*-
#import os
#import shutil
import tempfile

from django.contrib import admin
#from django.contrib.admin.actions import delete_selected as _delete_selected

from bumerang.apps.utils.admin import TitleSlugAdmin
from bumerang.apps.video.mediainfo import video_duration
from bumerang.apps.video.models import Video, VideoCategory, VideoGenre
from bumerang.apps.video.tasks import MakeScreenShots, ConvertVideoTask


class VideoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'get_owner_profile', 'duration',
                       'views_count', 'get_absolute_url')
    list_display = ('title', 'get_absolute_url', 'category',
                    'get_owner_profile', 'owner', 'status', 'created',
                    'published_in_archive', 'is_in_broadcast_lists')
    list_editable = ('category', 'published_in_archive',
                     'is_in_broadcast_lists')
    fieldsets = (
        (None, {'fields': (
            ('published_in_archive', 'is_in_broadcast_lists'),
            'title',
            ('get_owner_profile', 'owner'),
            'category',
            'album',
            'status',
            ('original_file', 'hq_file'),
        )}),
        ('Info options', {'fields': (
            ('year', 'genre'),
            ('country', 'city'),
            ('authors', 'teachers'),
            ('manager', 'agency'),
            'festivals',
            'description',
            'access',
        )}),
        ('Readonly options', {'fields': (
            'duration',
            'views_count',
        ), 'classes': ('collapse',)})
    )
    fields = (
    )
    actions = ['delete_selected']

    def get_duration(self, field):
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.write(field.file.read())
        field.file.seek(0)
        duration = video_duration(temp_file.name)
        temp_file.close()
        return duration

    def save_model(self, request, obj, form, change):
        if 'original_file' in form.changed_data:
            obj.status = obj.PENDING
            obj.save()
            ConvertVideoTask.delay(obj.id)
#        elif {'hq_file', 'mq_file', 'lq_file'} & set(form.changed_data):
        elif {'hq_file'} & set(form.changed_data):
            obj.duration = self.get_duration(obj.best_quality_file())
            if obj.duration:
                obj.status = Video.PENDING
                obj.save()
                MakeScreenShots.delay(obj.id)
            else:
                obj.status = Video.ERROR
                obj.save()
        else:
            obj.save()

#TODO: repair mass deleting
#    def delete_selected(self, request, queryset):
#        if request.POST.get('post'):
#            folders = [os.path.split(video.any_file().path)[0]
#                for video in queryset.all()
#                if video.any_file()
#            ]
#        result = _delete_selected(self, request, queryset)
#        if request.POST.get('post'):
#            for folder in folders:
#                shutil.rmtree(folder)
#        return result
#    delete_selected.short_description = u'Удалить вместе с файлами'


admin.site.register(Video, VideoAdmin)
admin.site.register(VideoGenre, TitleSlugAdmin)
admin.site.register(VideoCategory, TitleSlugAdmin)
# -*- coding: utf-8 -*-
from django.contrib import admin

from models import Photo, PhotoGenre


class PhotoAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ['original_file', 'created']
    list_display = ['title', 'created', 'owner',
                    'published_in_archive']
    list_editable = ['published_in_archive']


class TitleSlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoGenre, TitleSlugAdmin)
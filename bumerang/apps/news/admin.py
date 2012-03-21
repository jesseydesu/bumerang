# -*- coding: utf-8 -*-
from django.contrib import admin

from bumerang.apps.news.models import NewsCategory, NewsItem


class NewsCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class NewsItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

    class Media:
        js = [
            'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            'j/tinymce_setup.js',
        ]


admin.site.register(NewsCategory, NewsCategoryAdmin)
admin.site.register(NewsItem, NewsItemAdmin)